from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.app.db import get_db
from server.app.models import Task
from server.app.schemas import TaskCreate, TaskOut, TaskResult

router = APIRouter()


@router.post("/", response_model=TaskOut)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        type=task_data.type,
        payload=task_data.payload,
        assigned_node_id=task_data.assigned_node_id,
        status="pending",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/next/{node_id}", response_model=TaskOut)
def get_next_task(node_id: int, db: Session = Depends(get_db)):
    task = (
        db.query(Task)
        .filter(Task.assigned_node_id == node_id, Task.status == "pending")
        .order_by(Task.id.asc())
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="No pending tasks")

    task.status = "running"
    db.commit()
    db.refresh(task)
    return task


@router.post("/{task_id}/result", response_model=TaskOut)
def submit_task_result(task_id: int, task_result: TaskResult, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.result = task_result.result
    task.status = task_result.status
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task