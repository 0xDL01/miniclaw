# MiniClaw

> AI operator system that executes commands across devices.

MiniClaw is a cross-device AI operator designed to transform human commands into real system-level execution.

It is built around one core idea:  
AI should not only respond — it should act.

---

## Overview

MiniClaw connects human intent to execution through a modular architecture consisting of:

- a central orchestration system  
- device-level execution nodes  
- a voice-driven command interface  

The current version focuses on macOS-based command execution and system control.

---

## Core Capabilities

- Voice → Command → Execution pipeline  
- Open applications on macOS  
- Open URLs and web services  
- Centralized task routing via API  
- Device-based execution model  
- Extensible command architecture  

---

## Architecture

MiniClaw is structured into three primary layers:

### Core Server (FastAPI)
- Handles task creation and routing  
- Maintains system state  
- Acts as the central orchestration layer  

### Device Node (macOS Executor)
- Registers with the core system  
- Polls for assigned tasks  
- Executes system-level actions  

### Voice Interface
- Captures speech input  
- Converts commands into structured tasks  
- Sends tasks to the core system  

---

## Example Flow

A command such as:

Open Safari

is processed as:

Voice → Parsing → Task Creation → Routing → Execution

---

## Setup

Clone the repository:

```bash
git clone https://github.com/0xDL01/miniclaw.git
cd miniclaw

Create the main environment:

python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic httpx

Create the voice environment (Python 3.12 recommended):
python3.12 -m venv .venv-voice
source .venv-voice/bin/activate
pip install SpeechRecognition PyAudio httpx

Running the System
Start the core server:
source .venv/bin/activate
uvicorn server.app.main:app --reload

Start the macOS node in a new terminal:
source .venv/bin/activate
python -m mac_node.node

Start the voice interface in another terminal:
source .venv-voice/bin/activate
python -m voice.voice_command

Usage
Once all components are running, issue commands such as:
open safari
open github
open chrome
open finder
MiniClaw will:
Capture the command
Convert it into a structured task
Route it through the core system
Execute it on the connected device

Design Philosophy
MiniClaw is not a chatbot.
It is an execution system designed to:
convert intent into action
reduce manual interaction with systems
enable automation through natural commands

Roadmap
 Voice-based application execution
 URL command handling
 Application control (close / switch / manage)
 Screen understanding (OCR + context awareness)
 Multi-device orchestration
 Workflow automation engine


Status
Early-stage prototype (v0.1)
The current version demonstrates the core execution architecture.
Advanced capabilities and internal components are under active development and are not included in the public release.


Author
0xDL01



