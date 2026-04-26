from typing import Dict, List

from capea.schemas import ActionGraph
from capea.utils import stable_seed


ACTION_TEMPLATES = {
    "cut": "first-person POV kitchen scene, {action} {target}",
    "chop": "first-person POV kitchen scene, {action} {target}",
    "fry": "first-person POV kitchen scene, {action} {target}",
    "boil": "first-person POV kitchen scene, {action} {target}",
    "toast": "first-person POV kitchen scene, {action} {target}",
}


DEFAULT_STYLE = (
    "first-person egocentric POV kitchen scene, realistic hands interacting with objects, "
    "consistent kitchen environment, same lighting, same camera perspective, "
    "realistic cooking video frame, high detail, no text, no watermark"
)

class PromptBuilder:
    def __init__(self, graph: ActionGraph, base_seed: int = 42):
        self.graph = graph
        self.node_map = graph.node_map()
        self.base_seed = base_seed

    def build_prompts(self, schedule_result: Dict) -> List[Dict]:
        prompts = []

        for step in schedule_result.get("schedule", []):
            node = self.node_map[step["node_id"]]

            template = ACTION_TEMPLATES.get(
                node.action.lower(),
                "top-down POV cooking scene, {action} {target}"
            )

            base_prompt = template.format(
                action=node.action,
                target=node.target,
            )

            resource_phrase = ""
            if node.resources:
                resource_phrase = " using " + ", ".join(node.resources)

            full_prompt = f"{base_prompt}{resource_phrase}, {DEFAULT_STYLE}"

            seed_key = f"{node.id}:{','.join(node.resources)}"
            seed = stable_seed(seed_key, base_seed=self.base_seed)

            prompts.append(
                {
                    "node_id": node.id,
                    "action": node.action,
                    "target": node.target,
                    "start_time": step["start_time"],
                    "end_time": step["end_time"],
                    "resources": node.resources,
                    "prompt": full_prompt,
                    "negative_prompt": (
                        "inconsistent objects, changing background, distorted hands, "
                        "extra fingers, blurry, low quality, text, watermark"
                    ),
                    "seed": seed,
                    "output_keyframe": f"outputs_json/keyframes/{node.id}.png",
                    "output_clip": f"outputs_json/clips/{node.id}.mp4"
                }
            )

        return prompts