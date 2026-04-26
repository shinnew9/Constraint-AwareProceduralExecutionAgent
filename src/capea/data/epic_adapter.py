# This file tunrs EPIC CSV -> ActionGraph
import argparse
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from capea.schemas import ActionGraph, ActionNode
from capea.utils import make_node_id, write_json, ensure_dir


DEFAULT_RESOURCE_RULES: Dict[str, List[str]] = {
    "cut": ["knife", "cutting_board"],
    "chop": ["knife", "cutting_board"],
    "slice": ["knife", "cutting_board"],
    "peel": ["knife"],
    "wash": ["sink"],
    "rinse": ["sink"],
    "boil": ["stove", "pot"],
    "fry": ["stove", "pan"],
    "cook": ["stove", "pan"],
    "stir": ["spoon", "pan"],
    "mix": ["bowl", "spoon"],
    "pour": ["container"],
    "open": ["hand"],
"close": ["hand"],
"take": ["hand"],
"put": ["hand"],
"put-into": ["hand"],
"put-onto": ["hand"],
"turn-on": ["hand"],
"turn-off": ["hand"],
}


def _first_existing_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def infer_resources(action: str, target: str) -> List[str]:
    action = str(action).lower().strip()
    target = str(target).lower().strip()

    resources = list(DEFAULT_RESOURCE_RULES.get(action, []))

    # simple domain heuristics
    if target in {"egg", "onion", "garlic", "tomato", "potato"} and action in {"cut", "chop", "slice"}:
        for r in ["knife", "cutting_board"]:
            if r not in resources:
                resources.append(r)

    if target in {"water", "pasta", "rice"} and action in {"boil", "cook"}:
        for r in ["stove", "pot"]:
            if r not in resources:
                resources.append(r)

    return resources


def load_epic_csv(csv_path: str | Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    return pd.read_csv(csv_path)


def epic_rows_to_graph(
    df: pd.DataFrame,
    start_index: int = 0,
    window_size: int = 8,
    sequential_edges: bool = True,
) -> ActionGraph:
    verb_col = _first_existing_column(df, ["verb", "verb_name", "action"])
    noun_col = _first_existing_column(df, ["noun", "noun_name", "target", "object"])
    narration_col = _first_existing_column(df, ["narration", "sentence", "description"])
    start_col = _first_existing_column(df, ["start_timestamp", "start_time", "start_frame"])
    stop_col = _first_existing_column(df, ["stop_timestamp", "stop_time", "stop_frame"])

    if verb_col is None or noun_col is None:
        raise ValueError(
            f"Could not find required verb/noun columns. Available columns: {list(df.columns)}"
        )

    chunk = df.iloc[start_index : start_index + window_size].copy()

    nodes: List[ActionNode] = []
    edges = []

    for local_idx, (_, row) in enumerate(chunk.iterrows(), start=1):
        action = str(row[verb_col]).strip().lower()
        target = str(row[noun_col]).strip().lower()

        if action in {"nan", ""} or target in {"nan", ""}:
            continue

        node_id = make_node_id(action, target, local_idx)
        resources = infer_resources(action, target)

        preconditions = []
        effects = [f"{target}_{action}_done"]

        metadata = {}
        if narration_col:
            metadata["narration"] = str(row[narration_col])
        if start_col:
            metadata["start"] = str(row[start_col])
        if stop_col:
            metadata["stop"] = str(row[stop_col])

        nodes.append(
            ActionNode(
                id=node_id,
                action=action,
                target=target,
                duration=1,
                resources=resources,
                preconditions=preconditions,
                effects=effects,
            )
        )

    if sequential_edges:
        for i in range(len(nodes) - 1):
            edges.append((nodes[i].id, nodes[i + 1].id))

    return ActionGraph(nodes=nodes, edges=edges)


def convert_epic_csv_to_graph_json(
    csv_path: str | Path,
    output_path: str | Path,
    start_index: int = 0,
    window_size: int = 8,
    sequential_edges: bool = True,
) -> Path:
    df = load_epic_csv(csv_path)
    graph = epic_rows_to_graph(
        df=df,
        start_index=start_index,
        window_size=window_size,
        sequential_edges=sequential_edges,
    )

    output_path = Path(output_path)
    ensure_dir(output_path.parent)
    write_json(graph.model_dump(), output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Convert EPIC-KITCHENS annotation CSV to CAPEA ActionGraph JSON.")
    parser.add_argument("--csv", required=True, help="Path to EPIC_100_train.csv or EPIC_100_validation.csv")
    parser.add_argument("--output", required=True, help="Output ActionGraph JSON path")
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--window-size", type=int, default=8)
    parser.add_argument("--no-sequential-edges", action="store_true")

    args = parser.parse_args()

    output_path = convert_epic_csv_to_graph_json(
        csv_path=args.csv,
        output_path=args.output,
        start_index=args.start_index,
        window_size=args.window_size,
        sequential_edges=not args.no_sequential_edges,
    )

    print(f"Saved ActionGraph JSON to: {output_path}")


if __name__ == "__main__":
    main()