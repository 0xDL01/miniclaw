from server.app.db import Base, engine
from server.app.models import Node, Task  # noqa: F401

Base.metadata.create_all(bind=engine)
print("Database initialized.")