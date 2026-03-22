from pydantic import BaseModel
from typing import Optional


class NodeRegister(BaseModel):
    name: str
    platform: str


class NodeOut(BaseModel):
    id: int
    name: str
    platform: str
    status: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    type: str
    payload: str
    assigned_node_id: Optional[int] = None


class TaskOut(BaseModel):
    id: int
    type: str
    payload: str
    status: str
    assigned_node_id: Optional[int]
    result: Optional[str]

    class Config:
        from_attributes = True


class TaskResult(BaseModel):
    result: str
    status: str