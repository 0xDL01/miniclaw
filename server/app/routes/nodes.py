from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.app.db import get_db
from server.app.models import Node
from server.app.schemas import NodeRegister, NodeOut

router = APIRouter()


@router.post("/register", response_model=NodeOut)
def register_node(node_data: NodeRegister, db: Session = Depends(get_db)):
    node = Node(
        name=node_data.name,
        platform=node_data.platform,
        status="online",
    )
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


@router.get("/", response_model=list[NodeOut])
def list_nodes(db: Session = Depends(get_db)):
    return db.query(Node).order_by(Node.id.desc()).all()