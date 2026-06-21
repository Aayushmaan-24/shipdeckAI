import json
from typing import List, Dict, Any
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from backend.app.agents.workflow import app as workflow_app
from backend.app.utils.pptx_gen import generate_pptx

router = APIRouter()


class GenerateRequest(BaseModel):
    github_url: str


class DownloadRequest(BaseModel):
    slides: List[Dict[str, Any]]


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


@router.post("/download")
async def download_pptx(request: DownloadRequest):
    pptx_io = generate_pptx(request.slides)
    return Response(
        content=pptx_io.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={
            "Content-Disposition": "attachment; filename=pitch_deck.pptx"
        }
    )
