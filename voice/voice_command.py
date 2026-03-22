import json
import speech_recognition as sr
import httpx

SERVER_URL = "http://127.0.0.1:8000"

URL_ALIASES = {
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com",
    "chat": "https://chat.openai.com",
    "youtube": "https://youtube.com",
    "google": "https://google.com",
}

APP_CANONICAL = {
    "chrome": "Google Chrome",
    "brave": "Brave Browser",
    "brave browser": "Brave Browser",
    "finder": "Finder",
    "terminal": "Terminal",
    "notes": "Notes",
    "mail": "Mail",
    "messages": "Messages",
    "photos": "Photos",
    "maps": "Maps",
    "camera": "Photo Booth",
    "photo booth": "Photo Booth",
    "photobooth": "Photo Booth",
    "preview": "Preview",
    "safari": "Safari",
    "calculator": "Calculator",
    "reminders": "Reminders",
}


def normalize_text(text: str) -> str:
    t = text.lower().strip()

    replacements = {
        "git hub": "github",
        "g mail": "gmail",
        "photo booth": "photobooth",
        "my tose": "mythos",
        "mitosis": "mythos",
        "my toss": "mythos",
        "map": "maps",
    }

    for old, new in replacements.items():
        t = t.replace(old, new)

    return t


def to_title_app_name(target: str) -> str:
    return " ".join(word.capitalize() for word in target.split())


def parse_command(text: str):
    t = normalize_text(text)

    if "take screenshot" in t or "screenshot" in t:
        return {
            "type": "TAKE_SCREENSHOT",
            "payload": {"output_path": "/tmp/miniclaw_voice.png"},
        }

    if t.startswith("quit "):
        target = t.replace("quit ", "", 1).strip()
        app_name = APP_CANONICAL.get(target, to_title_app_name(target))
        return {
            "type": "QUIT_APP",
            "payload": {"app_name": app_name},
        }

    if t.startswith("close "):
        target = t.replace("close ", "", 1).strip()
        app_name = APP_CANONICAL.get(target, to_title_app_name(target))
        return {
            "type": "CLOSE_FRONT_WINDOW",
            "payload": {"app_name": app_name},
        }

    if t.startswith("open "):
        target = t.replace("open ", "", 1).strip()

        if target in URL_ALIASES:
            return {
                "type": "OPEN_URL",
                "payload": {"url": URL_ALIASES[target]},
            }

        if target == "mythos":
            return {
                "type": "OPEN_URL",
                "payload": {"url": "https://chat.openai.com"},
            }

        app_name = APP_CANONICAL.get(target, to_title_app_name(target))
        return {
            "type": "OPEN_APP",
            "payload": {"app_name": app_name},
        }

    return None


def get_latest_node_id():
    response = httpx.get(f"{SERVER_URL}/nodes/", timeout=10.0)
    response.raise_for_status()
    nodes = response.json()

    if not nodes:
        raise RuntimeError("No nodes found. Start the mac node first.")

    latest_node = nodes[0]
    print(f"Using node id={latest_node['id']} name={latest_node['name']}")
    return latest_node["id"]


def create_task(node_id: int, task_type: str, payload: dict):
    response = httpx.post(
        f"{SERVER_URL}/tasks/",
        json={
            "type": task_type,
            "payload": json.dumps(payload),
            "assigned_node_id": node_id,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()


def listen_once(recognizer):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as exc:
        print(f"Speech service error: {exc}")
        return None


def main():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("MiniClaw voice loop started. Press Ctrl+C to stop.")

    node_id = get_latest_node_id()

    while True:
        text = listen_once(recognizer)
        if not text:
            continue

        task = parse_command(text)
        if not task:
            print("No matching command found.")
            continue

        try:
            created = create_task(node_id, task["type"], task["payload"])
            print(f"Task created: {created}")
        except Exception as exc:
            print(f"Failed to create task: {exc}")


if __name__ == "__main__":
    main()