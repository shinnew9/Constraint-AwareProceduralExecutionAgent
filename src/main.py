from agent import generate_action_graph
from simulator import verify_and_schedule
from generator import simulate_video_rendering

def main():
    # Example input with temporal and resource overlaps
    user_request = (
        "I want to make ramen. First, chop the onions. "
        "Then boil water in a pot on stove_1. Once the water is boiling, "
        "add the noodles. I also need to fry an egg on stove_1 while the noodles cook."
    )

    print("Step 1: Parsing Natural Instructions into Action Graph...")
    graph = generate_action_graph(user_request)
    print(f"Project: {graph.title}\n")

    print("Step 2: Simulating Constraints & Scheduling...")
    final_schedule = verify_and_schedule(graph)

    print("-" * 50)
    print(f"{'TIME':<15} | {'ACTION':<25} | {'RESOURCE'}")
    print("-" * 50)
    for step in final_schedule:
        time_range = f"{step['start']}s - {step['end']}s"
        print(f"{time_range:<15} | {step['action']:<25} | {step['resource']}")

    final_dish_step = {
        'id': 5,
        'action': 'serve dish',
        'resource': 'dining_table'
    }
    final_schedule.append(final_dish_step)

    print("\nStep 3: Generating Video Sequence...")
    simulate_video_rendering(final_schedule)

if __name__ == "__main__":
    main()