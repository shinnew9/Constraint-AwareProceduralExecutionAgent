import glob

from capea.utils import read_json
from capea.evaluation.metrics import constraint_violation_rate


def main():
    files = glob.glob("outputs_json/schedules/*.json")

    results = []
    for f in files:
        data = read_json(f)
        results.append(data)

    rate = constraint_violation_rate(results)

    print("\n=== Evaluation ===")
    print(f"Constraint Violation Rate: {rate:.2f}")


if __name__ == "__main__":
    main()