from sqlalchemy import Column, Integer, String, Text
from server.app.db import Base


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    status = Column(String, default="online")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    status = Column(String, default="pending")
    assigned_node_id = Column(Integer, nullable=True)
    result = Column(Text, nullable=True)