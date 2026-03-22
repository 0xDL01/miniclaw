import json
import subprocess


def execute_task(task_type: str, payload: str) -> str:
    data = json.loads(payload)

    if task_type == "OPEN_APP":
        app_name = data["app_name"]
        subprocess.run(["open", "-a", app_name], check=True)
        return f"Opened app: {app_name}"

    if task_type == "OPEN_URL":
        url = data["url"]
        subprocess.run(["open", url], check=True)
        return f"Opened URL: {url}"

    if task_type == "TAKE_SCREENSHOT":
        output_path = data.get("output_path", "/tmp/miniclaw_screenshot.png")
        subprocess.run(["screencapture", "-x", output_path], check=True)
        return f"Screenshot saved to: {output_path}"

    raise ValueError(f"Unsupported task type: {task_type}")