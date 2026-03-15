import networkx as nx
import matplotlib.pyplot as plt
from schemas import ActionGraph

def verify_and_schedule(action_graph: ActionGraph):
    """
    Calculates execution timeline and visualizes it as a Gantt Chart.
    """
    G = nx.DiGraph()
    nodes_data = {node.id: node for node in action_graph.nodes}
    
    for node in action_graph.nodes:
        G.add_node(node.id)
        for dep in node.depends_on:
            G.add_edge(dep, node.id)

    resource_free_at = {}
    task_end_times = {}
    scheduled_output = []

    for node_id in nx.topological_sort(G):
        node = nodes_data[node_id]
        dep_ready_time = max([task_end_times.get(d, 0) for d in G.predecessors(node_id)] + [0])
        res_ready_time = resource_free_at.get(node.resource, 0)
        
        actual_start = max(dep_ready_time, res_ready_time)
        actual_end = actual_start + node.duration
        
        task_end_times[node_id] = actual_end
        resource_free_at[node.resource] = actual_end
        
        scheduled_output.append({
            "id": node_id,
            "action": f"{node.action} {node.target}",
            "start": actual_start,
            "end": actual_end,
            "resource": node.resource
        })
    
    # Visualization (Gantt Chart)
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, step in enumerate(scheduled_output):
        ax.broken_barh([(step['start'], step['end'] - step['start'])], 
                       (i*10, 9), facecolors='tab:blue')
        ax.text(step['start'], i*10 + 5, f"  {step['action']} ({step['resource']})", va='center')

    ax.set_xlabel('Time (seconds)')
    ax.set_yticks([i*10 + 5 for i in range(len(scheduled_output))])
    ax.set_yticklabels([f"Step {s['id']}" for s in scheduled_output])
    
    
    
    plt.title("Constraint-Aware Execution Timeline")
    plt.tight_layout()
    
    # plt.show() 대신 파일로 저장!
    plt.savefig('timeline.png') 
    print("Timeline chart saved as 'timeline.png'")
    
    return scheduled_output

    return scheduled_output