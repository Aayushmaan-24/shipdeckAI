import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.app.agents.workflow import app as workflow_app

router = APIRouter()

class GenerateRequest(BaseModel):
    github_url: str

async def generate_stream(github_url: str):
    initial_state = {
        "messages": [f"Started generation for {github_url}"],
        "repo_path": github_url,
        "code_summary": "",
        "business_narrative": "",
        "deck_structure": [],
        "visual_assets": [],
        "next_step": ""
    }

    # Using stream to provide "real-time streaming progress" as per PRD
    async for event in workflow_app.astream(initial_state):
        # Flatten the event for the frontend
        yield f"data: {json.dumps(event)}\n\n"

@router.post("/generate")
async def generate_deck(request: GenerateRequest):
    return StreamingResponse(
        generate_stream(request.github_url),
        media_type="text/event-stream"
    )
