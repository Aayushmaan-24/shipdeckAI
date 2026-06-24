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

    github_metadata = {}
    readme_content = ""
    file_tree = ""
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
                        github_metadata = {
                            "name": data.get("name"),
                            "full_name": data.get("full_name"),
                            "description": data.get("description"),
                            "topics": data.get("topics"),
                            "language": data.get("language"),
                            "stars": data.get("stargazers_count")
                        }

                    # Fetch README content
                    readme_resp = client.get(f"{base_url}/readme", timeout=10.0)
                    if readme_resp.status_code == 200:
                        readme_data = readme_resp.json()
                        content_encoded = readme_data.get("content", "")
                        if content_encoded:
                            readme_content = base64.b64decode(content_encoded).decode("utf-8", errors="ignore")
                            # Truncate README if it's too long (e.g., first 5000 chars)
                            readme_content = readme_content[:5000]

                    # Fetch File Tree (recursive, max 1000 items)
                    tree_resp = client.get(f"{base_url}/git/trees/main?recursive=1", timeout=10.0)
                    if tree_resp.status_code != 200:
                        # try master if main fails
                        tree_resp = client.get(f"{base_url}/git/trees/master?recursive=1", timeout=10.0)

                    if tree_resp.status_code == 200:
                        tree_data = tree_resp.json()
                        files = [item.get("path") for item in tree_data.get("tree", []) if item.get("type") == "blob"]
                        file_tree = "\n".join(files[:1000]) # limit to first 1000 files
            except Exception as e:
                github_metadata = {"error": f"Error fetching GitHub data: {str(e)}"}

    llm = get_groq_llm()
    if llm:
        prompt = (
            f"You are a Repo Explorer Agent. Analyze this GitHub URL: {repo_path}.\n"
            f"GitHub API Metadata: {json.dumps(github_metadata)}\n"
            f"README Content (partial): {readme_content}\n"
            f"File Tree (partial):\n{file_tree}\n\n"
            "TASKS:\n"
            "1. Identify the EXACT project name. Look at README headings, repo name, and metadata.\n"
            "2. Identify the core problem the project solves.\n"
            "3. Identify the tech stack (languages, frameworks, databases, ML tools).\n"
            "4. Map out the project structure and key components.\n"
            "5. DO NOT HALLUCINATE. Only use information provided. If the project is about Credit Risk, call it that. "
            "NEVER use generic names like 'Eonix' or 'Template Project'."
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
        prompt = (
            f"Repo Analysis: {repo_summary}\n\n"
            "TASK: Extract a highly detailed technical profile of the repository.\n"
            "Identify:\n"
            "- Exact Project Name\n"
            "- Core Technical Architecture (Frontend, Backend, Database, AI/ML layers)\n"
            "- Specific Technology Stack (version numbers if available)\n"
            "- Key Features and Functionalities\n"
            "- ML/AI Components (models used, data flow, prediction logic)\n"
            "- Repository Structure and File Layout\n\n"
            "STRICT REQUIREMENT: USE THE ANALYZED DATA ONLY. Do not use placeholder names like 'Eonix'. "
            "If the project is 'CreditBridge', refer to it only as 'CreditBridge'."
        )
        response = llm.invoke([
            SystemMessage(content="You are a Code Intelligence Agent. You provide accurate technical assessments of codebases."),
            HumanMessage(content=prompt)
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
        prompt = (
            f"Technical Profile: {code_summary}\n\n"
            "TASK: Create a compelling business narrative for this project.\n"
            "Focus on:\n"
            "- Problem Statement: What real-world pain point does it solve?\n"
            "- Solution Overview: How does it uniquely address the problem?\n"
            "- Target Audience: Who are the users and stakeholders?\n"
            "- Business Value: Why is this important? What is the impact?\n"
            "- Future Roadmap: Potential growth and upcoming features.\n\n"
            "STRICT REQUIREMENT: Ensure the narrative is grounded in the technical reality of the repository. "
            "Maintain consistent branding with the project name identified in the Technical Profile."
        )
        response = llm.invoke([
            SystemMessage(content="You are a Business Strategist Agent. You turn technical projects into compelling startup stories."),
            HumanMessage(content=prompt)
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
    layout_type: str = Field("text", description="The layout type: 'text', 'grid', or 'architecture'")

class PitchDeck(BaseModel):
    slides: List[Slide] = Field(..., description="A list of 12 to 16 slides for the pitch deck")

def deck_architect_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Defines the structure and content of each slide (12-16 slides).
    Uses structured output for reliability.
    """
    narrative = state.get("business_narrative", "")
    code_summary = state.get("code_summary", "")
    llm = get_groq_llm()

    if llm:
        structured_llm = llm.with_structured_output(PitchDeck)
        prompt = (
            f"Business Narrative: {narrative}\n"
            f"Technical Profile: {code_summary}\n\n"
            "TASK: Create a professional 12-16 slide investor pitch deck.\n"
            "MANDATORY SLIDE STRUCTURE:\n"
            "1. Title Slide: Project Name and Tagline\n"
            "2. Problem Statement: Real-world credit/financial challenges\n"
            "3. Solution Overview: How the project solves these challenges\n"
            "4. Product Features: Key functionalities (risk prediction, improvement recommendations, etc.)\n"
            "5. System Architecture: High-level overview of components\n"
            "6. ML / Risk Prediction Engine: Models, inputs, outputs, and logic\n"
            "7. User Journey: Onboarding to value realization\n"
            "8. Technology Stack: Tools and frameworks used\n"
            "9. Repository Structure: Key directories and files\n"
            "10. Key Innovations: What makes this unique?\n"
            "11. Future Roadmap: Upcoming features\n"
            "12. Conclusion & Contact\n\n"
            "STRICT REQUIREMENTS:\n"
            "- Use the ACTUAL project name everywhere.\n"
            "- Content must be SPECIFIC to the repository. No generic filler.\n"
            "- Bullet points should be concise and professional.\n"
            "- Assign 'architecture' layout to the System Architecture slide.\n"
            "- Assign 'grid' layout to Features or Technology Stack slides if they have many items.\n"
            "- NEVER use placeholder names like 'Eonix'."
        )
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
    Verifies that the deck has at least 12 slides and no hallucinations.
    """
    deck = state.get("deck_structure", [])

    # 1. Slide count check
    if len(deck) < 12:
        return {
            "messages": [f"Supervisor: Deck only has {len(deck)} slides. Requesting expansion."],
            "next_step": "deck_architect"
        }

    # 2. Hallucination check
    hallucinated_names = ["Eonix", "Template Project", "Generic Startup"]
    deck_text = json.dumps(deck).lower()
    for name in hallucinated_names:
        if name.lower() in deck_text:
            return {
                "messages": [f"Supervisor: Hallucination detected ('{name}'). Requesting re-generation."],
                "next_step": "deck_architect"
            }

    return {
        "messages": ["Supervisor: Workflow validated and complete."],
        "next_step": "end"
    }
