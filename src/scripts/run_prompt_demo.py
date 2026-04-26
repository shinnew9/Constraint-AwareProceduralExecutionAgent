import os
import sys

from capea.schemas import ActionGraph
from capea.utils import read_json, write_json, ensure_dir, log
from capea.execution.simulator import ExecutionSimulator
from capea.visual.prompt_builder import PromptBuilder


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/scripts/run_prompt_demo.py <path_to_example_json>")
        sys.exit(1)

    input_path = sys.argv[1]
    filename = os.path.basename(input_path).replace(".json", "")

    log(f"Loading graph from {input_path}")
    data = read_json(input_path)
    graph = ActionGraph(**data)

    log("Running schedule simulation")
    simulator = ExecutionSimulator(graph)
    schedule_result = simulator.run()

    if not schedule_result["success"]:
        print("\nGraph is invalid. Stop before prompt generation.")
        print(schedule_result["issues"])
        return

    log("Building generation prompts")
    builder = PromptBuilder(graph)
    prompts = builder.build_prompts(schedule_result)

    output_dir = ensure_dir("outputs_json/prompts")
    output_path = output_dir / f"{filename}_prompts.json"

    write_json(
        {
            "source": input_path,
            "schedule": schedule_result,
            "prompts": prompts,
        },
        output_path,
    )

    print(f"\nSaved prompts to: {output_path}")
    print("\n=== Generated Prompts ===")
    for item in prompts:
        print(f"\n[{item['node_id']}] seed={item['seed']}")
        print(item["prompt"])


if __name__ == "__main__":
    main()