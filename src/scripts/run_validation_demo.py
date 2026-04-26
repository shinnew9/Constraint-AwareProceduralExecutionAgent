import os
import sys

from capea.schemas import ActionGraph
from capea.utils import read_json, write_json, ensure_dir, log
from capea.logic.validator import DAGValidator
from capea.execution.simulator import ExecutionSimulator


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/scripts/run_validation_demo.py <path_to_example_json>")
        sys.exit(1)

    input_path = sys.argv[1]

    log(f"Loading graph from {input_path}")
    data = read_json(input_path)
    graph = ActionGraph(**data)

    log("Running DAG validation")
    validator = DAGValidator(graph)
    report = validator.validate()

    print("\n=== Validation Report ===")
    print(report.model_dump_json(indent=2))

    if not report.is_valid:
        print("\nGraph is invalid. Stop before simulation.")
        return

    log("Running execution simulation")
    simulator = ExecutionSimulator(graph)
    result = simulator.run()

    print("\n=== Simulation Result ===")
    print(result)

    # Save schedule result automatically
    filename = os.path.basename(input_path).replace(".json", "")
    output_name = f"{filename}_schedule.json"

    output_dir = ensure_dir("outputs_json/schedules")
    output_path = output_dir / output_name

    write_json(result, output_path)
    print(f"\nSaved schedule to: {output_path}")


if __name__ == "__main__":
    main()