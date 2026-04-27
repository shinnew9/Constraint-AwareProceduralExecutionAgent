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

    def build_prompt(self, node):
        action = node["action"]
        target = node["target"]

        if action in ["open", "close"]:
            action_phrase = f"opening a {target} door, hand on handle"
        elif action in ["cut", "chop"]:
            action_phrase = f"cutting {target} with a knife, hand holding knife"
        elif action in ["pour"]:
            action_phrase = f"pouring into {target}, liquid visible"
        elif action in ["take"]:
            action_phrase = f"picking up a {target} with hand"
        else:
            action_phrase = f"{action} a {target}"

        prompt = (
            f"a person {action_phrase}, "
            f"mid-action, motion visible, "
            f"realistic kitchen scene, "
            f"top-down POV, consistent environment, "
            f"same lighting, same camera angle, "
            f"high detail, no text, no watermark"
        )

        return prompt