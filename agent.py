import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater")

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from pathlib import Path
import tempfile
import re
from typing import Optional, Iterable, Any

load_dotenv()

NOTES_DIR = Path(os.getenv("NOTES_DIR", Path(tempfile.gettempdir()) / "notes")).resolve()
NOTES_DIR.mkdir(parents=True, exist_ok=True)


def get_note_path(filepath: str) -> Path:
    return _note_path(filepath)


def _note_path(filepath: str) -> Path:
    # Force notes to stay in a writable directory.
    filename = Path(filepath).name
    return (NOTES_DIR / filename).resolve()


@tool
def read_note(filepath: str) -> str:
    """Read the contents of a note stored in the notes directory."""
    try:
        path = _note_path(filepath)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Contents of '{path.name}':\n{content}"
    except FileNotFoundError:
        return f"Error: Note '{Path(filepath).name}' not found."
    except Exception as e:
        return f"Error reading note: {str(e)}"


@tool
def write_note(filepath: str, content: str) -> str:
    """Write content to a note in the notes directory."""
    try:
        path = _note_path(filepath)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{path.name}'."
    except Exception as e:
        return f"Error writing note: {str(e)}"


def _extract_saved_filename(messages: Iterable[Any]) -> Optional[str]:
    for message in reversed(list(messages)):
        content = None
        if isinstance(message, dict):
            content = message.get("content")
        else:
            content = getattr(message, "content", None)
        if not content:
            continue
        match = re.search(r"Successfully wrote \d+ characters to '([^']+)'\.", str(content))
        if match:
            return match.group(1)
    return None


TOOLS = [read_note, write_note]

SYSTEM_MESSAGE = (
    "You are a helpful note-taking assistant. "
    "You can read and write text files to help users manage their notes. "
    "Be concise and helpful."
)

llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14", temperature=0)
# agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_MESSAGE)
agent = create_agent(llm, TOOLS, system_prompt=SYSTEM_MESSAGE)


def run_agent(user_input: str) -> dict:
    """Run the agent with a user query and return the response plus metadata."""
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"recursion_limit": 50}
        )
        filename = _extract_saved_filename(result.get("messages", []))
        return {"response": result["messages"][-1].content, "filename": filename}
    except Exception as e:
        return {"response": f"Error: {str(e)}", "filename": None}
