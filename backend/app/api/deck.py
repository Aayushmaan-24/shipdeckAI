import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.app.agents.workflow import app as workflow_app

router = APIRouter()


class GenerateRequest(BaseModel):
    github_url: str


async def generate_stream(github_url: str):
    if not github_url.startswith("https://github.com/"):
        yield f"data: {json.dumps({'error': 'Invalid GitHub URL. Must start with https://github.com/'})}\n\n"
        return

    initial_state = {
        "messages": [f"Started generation for {github_url}"],
        "repo_path": github_url,
        "code_summary": "",
        "business_narrative": "",
        "deck_structure": [],
        "visual_assets": [],
        "next_step": "",
    }

    try:
        async for event in workflow_app.astream(initial_state):
            yield f"data: {json.dumps(event)}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@router.post("/generate")
async def generate_deck(request: GenerateRequest):
    return StreamingResponse(
        generate_stream(request.github_url),
        media_type="text/event-stream",
    )
