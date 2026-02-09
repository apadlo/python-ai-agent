from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import FileResponse
from agent import run_agent, get_note_path
from pathlib import Path
from typing import Optional

# import uvicorn

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Request model
class AgentRequest(BaseModel):
    """Request model for agent invocation."""
    prompt: str


# Response model
class AgentResponse(BaseModel):
    """Response model for agent invocation."""
    response: str
    filename: Optional[str] = None
    download_url: Optional[str] = None


@app.get("/")
async def home(request: Request):
    """Serve the main HTML interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/agent", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    """
    Invoke the AI agent with a prompt.

    The agent can read and write text files based on natural language instructions.
    """
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # Run the agent with the user's prompt
        result = run_agent(request.prompt)

        filename = result.get("filename")
        download_url = f"/download/{filename}" if filename else None

        return AgentResponse(response=result["response"], filename=filename, download_url=download_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking agent: {str(e)}")


@app.get("/download/{filename}")
async def download_note(filename: str):
    path = get_note_path(filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Note not found")
    return FileResponse(path, filename=path.name, media_type="text/plain")


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
