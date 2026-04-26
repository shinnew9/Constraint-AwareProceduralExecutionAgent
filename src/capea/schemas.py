from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class ActionNode(BaseModel):
    id: str
    action: str
    target: str
    duration: int = 1
    resources: List[str] = Field(default_factory=list)
    preconditions: List[str] = Field(default_factory=list)
    effects: List[str] = Field(default_factory=list)


class ActionGraph(BaseModel):
    nodes: List[ActionNode]
    edges: List[Tuple[str, str]] = Field(default_factory=list)

    def node_ids(self) -> List[str]:
        return [node.id for node in self.nodes]

    def node_map(self) -> Dict[str, ActionNode]:
        return {node.id: node for node in self.nodes}


class ScheduledStep(BaseModel):
    node_id: str
    start_time: int
    end_time: int
    resources: List[str] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    level: str = "error"
    code: str
    message: str
    node_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)


class ValidationReport(BaseModel):
    is_valid: bool
    issues: List[ValidationIssue] = Field(default_factory=list)

    def add_issue(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)
        if issue.level == "error":
            self.is_valid = False