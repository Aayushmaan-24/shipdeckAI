import os
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

def get_groq_llm(model_name="llama-3.3-70b-versatile"):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return ChatGroq(
        model=model_name,
        temperature=0.1,
        groq_api_key=api_key
    )

def get_gemini_llm(model_name="gemini-1.5-flash"):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.1,
        google_api_key=api_key
    )

def repo_explorer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Navigates and understands the repository structure.
    """
    repo_path = state.get("repo_path", "unknown")
    llm = get_groq_llm()

    if llm:
        response = llm.invoke([
            SystemMessage(content="You are a Repo Explorer Agent. Analyze the repo path and simulate exploration."),
            HumanMessage(content=f"Explore this repo: {repo_path}")
        ])
        summary = response.content
    else:
        summary = f"Mocked Exploration: Repository at {repo_path} analyzed."

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
            SystemMessage(content="You are a Code Intelligence Agent. Extract tech stack and features from the summary."),
            HumanMessage(content=f"Summary: {repo_summary}")
        ])
        code_summary = response.content
    else:
        code_summary = "Tech Stack: Next.js, FastAPI. Features: Pitch deck generation."

    return {
        "messages": ["Code Intelligence: Analysis complete."],
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
            SystemMessage(content="You are a Business Strategist Agent. Create a pitch narrative."),
            HumanMessage(content=f"Code Info: {code_summary}")
        ])
        narrative = response.content
    else:
        narrative = f"ShipDeck leverages {code_summary} to automate deck creation."

    return {
        "messages": ["Business Strategist: Synthesized business narrative."],
        "business_narrative": narrative,
        "next_step": "deck_architect"
    }

def deck_architect_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Defines the structure and content of each slide.
    """
    narrative = state.get("business_narrative", "")
    llm = get_gemini_llm() # Using Gemini for architect as per variety in PRD

    if llm:
        response = llm.invoke([
            SystemMessage(content="You are a Deck Architect. Outline 3 slides based on the narrative."),
            HumanMessage(content=f"Narrative: {narrative}")
        ])
        # For simplicity in prototype, we keep a structured mock but content from LLM
        deck_structure = [
            {"slide": 1, "title": "Overview", "content": response.content[:100]},
            {"slide": 2, "title": "The Narrative", "content": narrative[:100]},
            {"slide": 3, "title": "Next Steps", "content": "Development Roadmap"}
        ]
    else:
        deck_structure = [
            {"slide": 1, "title": "ShipDeck", "content": "From Code to Deck"},
            {"slide": 2, "title": "Narrative", "content": narrative[:100]}
        ]

    return {
        "messages": ["Deck Architect: Designed slide structure."],
        "deck_structure": deck_structure,
        "next_step": "visual_design"
    }

def visual_design_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates diagrams, icons, and layout specifications.
    """
    visual_assets = ["logo.png", "architecture_diagram.svg"]

    return {
        "messages": ["Visual Design: Assets defined."],
        "visual_assets": visual_assets,
        "next_step": "supervisor"
    }

def supervisor_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrates the workflow.
    """
    return {
        "messages": ["Supervisor: Workflow complete."],
        "next_step": "end"
    }
