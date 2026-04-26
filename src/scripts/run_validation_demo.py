from capea.schemas import ActionGraph, ActionNode
from capea.execution.simulator import ExecutionSimulator


def main():
    graph = ActionGraph(
        title="Ramen demo",
        nodes=[
            ActionNode(id=1, action="chop", target="onion", duration=10, resource="knife_1"),
            ActionNode(id=2, action="boil", target="water", duration=30, resource="stove_1"),
            ActionNode(id=3, action="fry", target="egg", duration=20, resource="stove_1"),
            ActionNode(id=4, action="serve", target="ramen", duration=5, resource="plate_1", depends_on=[1, 2, 3]),
        ],
    )
    result = ExecutionSimulator(graph).run()
    print("success:", result["success"])
    print("makespan:", result["makespan"])
    for step in result["schedule"]:
        print(step.model_dump())
    for issue in result["issues"]:
        print(issue.model_dump())


if __name__ == "__main__":
    main()
