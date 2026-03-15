from pydantic import BaseModel, Field
from typing import List, Optional

class ActionNode(BaseModel):
    id: int
    action: str = Field(..., description="Unique identifier for the action")
    target: str = Field(..., description="The verb/action (e.g., chop, boil, fry)")
    duration: int = Field(..., description="The object being acted upon (e.g., onion, water)")
    resource: str = Field(..., description="The primary tool.resource needed (e.g., knife, stove_1, pot)")
    depends_on: List[int] = Field(default_factory=list, description="IDs of tasks that must be finished first")

class ActionGraph(BaseModel):
    title: str = Field(..., description="Title of the cooking project")
    nodes: List[ActionNode] = Field(..., description="List of all execution steps")
    