import os
import json
import re
import httpx
import base64
from typing import List, Dict, Any
from pydantic import BaseModel, Field


def parse_json_from_llm(content: str):
    """Parse JSON from LLM output, stripping markdown code fences if present."""
    text = content.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    return json.loads(text)
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

def get_groq_llm(model_name="llama-3.3-70b-versatile"):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please add it to your .env file.")
    return ChatGroq(
        model=model_name,
        temperature=0.1,
        groq_api_key=api_key
    )

def get_gemini_llm(model_name="gemini-1.5-flash"):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set. Please add it to your .env file.")
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.1,
        google_api_key=api_key
    )

def repo_explorer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Navigates and understands the repository structure using GitHub API.
    """
    repo_path = state.get("repo_path", "unknown")

    github_metadata = ""
    readme_content = ""
    if "github.com" in repo_path:
        match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_path)
        if match:
            owner, repo = match.groups()
            repo = repo.split("?")[0].split("#")[0].replace(".git", "")
            base_url = f"https://api.github.com/repos/{owner}/{repo}"

            try:
                with httpx.Client() as client:
                    # Fetch basic metadata
                    resp = client.get(base_url, timeout=10.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        github_metadata = json.dumps({
                            "name": data.get("name"),
                            "description": data.get("description"),
                            "topics": data.get("topics"),
                            "language": data.get("language"),
                            "stars": data.get("stargazers_count")
                        })

                    # Fetch README content
                    readme_resp = client.get(f"{base_url}/readme", timeout=10.0)
                    if readme_resp.status_code == 200:
                        readme_data = readme_resp.json()
                        content_encoded = readme_data.get("content", "")
                        if content_encoded:
                            readme_content = base64.b64decode(content_encoded).decode("utf-8", errors="ignore")
                            # Truncate README if it's too long (e.g., first 5000 chars)
                            readme_content = readme_content[:5000]
            except Exception as e:
                github_metadata = f"Error fetching GitHub data: {str(e)}"

    llm = get_groq_llm()
    if llm:
        prompt = (
            f"You are a Repo Explorer Agent. Analyze this GitHub URL: {repo_path}.\n"
            f"GitHub API Metadata: {github_metadata}\n"
            f"README Content (partial): {readme_content}\n\n"
            "Identify tech stack, project structure, and key entry points. "
            "USE THE PROVIDED README CONTENT TO AVOID HALLUCINATIONS."
        )
        response = llm.invoke([
            SystemMessage(content="You are a senior software architect analyzing codebases."),
            HumanMessage(content=prompt)
        ])
        summary = response.content
    else:
        summary = f"Exploration of {repo_path}. Metadata: {github_metadata or 'None'}"

    return {
        "messages": [f"Repo Explorer: {summary}"],
        "next_step": "code_intelligence"
    }

def code_intelligence_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts technical stack, architecture, and core features.
    """
    repo_summary = state["messages"][-1]
    llm = get_groq_llm()

    if llm:
        response = llm.invoke([
            SystemMessage(content="You are a Code Intelligence Agent. Extract a structured tech stack and feature list."),
            HumanMessage(content=f"Repo Analysis: {repo_summary}")
        ])
        code_summary = response.content
    else:
        code_summary = "Stack: React, FastAPI. Features: Authentication, API, Database."

    return {
        "messages": ["Code Intelligence: Successfully extracted tech stack and features."],
        "code_summary": code_summary,
        "next_step": "business_strategist"
    }

def business_strategist_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes the value proposition and business narrative.
    """
    code_summary = state.get("code_summary", "")
    llm = get_groq_llm()

    if llm:
        response = llm.invoke([
            SystemMessage(content="You are a Business Strategist Agent. Create a compelling startup narrative."),
            HumanMessage(content=f"Technical capabilities: {code_summary}")
        ])
        narrative = response.content
    else:
        narrative = "ShipDeck transforms your code into a story."

    return {
        "messages": ["Business Strategist: Synthesized business narrative."],
        "business_narrative": narrative,
        "next_step": "deck_architect"
    }

class Slide(BaseModel):
    slide: int = Field(..., description="The slide number")
    title: str = Field(..., description="The title of the slide")
    content: str = Field(..., description="Detailed content for the slide")

class PitchDeck(BaseModel):
    slides: List[Slide] = Field(..., description="A list of 12 to 16 slides for the pitch deck")

def deck_architect_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Defines the structure and content of each slide (12-16 slides).
    Uses structured output for reliability.
    """
    narrative = state.get("business_narrative", "")
    llm = get_groq_llm()

    if llm:
        structured_llm = llm.with_structured_output(PitchDeck)
        prompt = f"Based on this narrative: '{narrative}', create a detailed investor pitch deck with 12-16 slides."
        try:
            result = structured_llm.invoke([
                SystemMessage(content="You are a Deck Architect specialized in structured investor pitches."),
                HumanMessage(content=prompt)
            ])
            deck_structure = [slide.model_dump() for slide in result.slides]
        except Exception as e:
            # Fallback
            deck_structure = [{"slide": i+1, "title": f"Slide {i+1}", "content": f"Error: {str(e)}"} for i in range(12)]
    else:
        deck_structure = [{"slide": i+1, "title": f"Slide {i+1}", "content": "Draft content"} for i in range(12)]

    return {
        "messages": [f"Deck Architect: Designed {len(deck_structure)} slides."],
        "deck_structure": deck_structure,
        "next_step": "supervisor"
    }

def supervisor_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrates the workflow and ensures quality/consistency.
    Verifies that the deck has at least 12 slides.
    """
    deck = state.get("deck_structure", [])
    if len(deck) < 12:
        return {
            "messages": [f"Supervisor: Deck only has {len(deck)} slides. Requesting expansion."],
            "next_step": "deck_architect"
        }

    return {
        "messages": ["Supervisor: Workflow validated and complete."],
        "next_step": "end"
    }
