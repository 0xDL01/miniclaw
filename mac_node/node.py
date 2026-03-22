import time
import httpx

from mac_node.config import SERVER_URL, NODE_NAME, PLATFORM, POLL_INTERVAL
from mac_node.executor import execute_task


def register_node() -> int:
    response = httpx.post(
        f"{SERVER_URL}/nodes/register",
        json={
            "name": NODE_NAME,
            "platform": PLATFORM,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    data = response.json()
    return data["id"]


def get_next_task(node_id: int):
    response = httpx.get(f"{SERVER_URL}/tasks/next/{node_id}", timeout=10.0)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def submit_result(task_id: int, result: str, status: str):
    response = httpx.post(
        f"{SERVER_URL}/tasks/{task_id}/result",
        json={
            "result": result,
            "status": status,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()


def main():
    node_id = register_node()
    print(f"[MiniClaw] Registered Mac node with id={node_id}")

    while True:
        try:
            task = get_next_task(node_id)
            if task:
                print(f"[MiniClaw] Received task: {task}")
                try:
                    result = execute_task(task["type"], task["payload"])
                    submit_result(task["id"], result, "completed")
                    print(f"[MiniClaw] Task {task['id']} completed: {result}")
                except Exception as exc:
                    submit_result(task["id"], str(exc), "failed")
                    print(f"[MiniClaw] Task {task['id']} failed: {exc}")
        except Exception as exc:
            print(f"[MiniClaw] Loop error: {exc}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()