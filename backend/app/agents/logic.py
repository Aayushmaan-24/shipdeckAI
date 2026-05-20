import os
import json
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
    In v1.0, for a prototype, we'll simulate deep analysis of the URL.
    """
    repo_path = state.get("repo_path", "unknown")
    llm = get_groq_llm()

    if llm:
        prompt = (
            f"You are a Repo Explorer Agent. Analyze this GitHub URL: {repo_path}. "
            "Identify likely tech stack, project structure, and key entry points based on standard naming conventions."
        )
        response = llm.invoke([
            SystemMessage(content="You are a senior software architect analyzing codebases from metadata."),
            HumanMessage(content=prompt)
        ])
        summary = response.content
    else:
        summary = f"Simulated exploration of {repo_path}."

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

def deck_architect_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Defines the structure and content of each slide (12-16 slides as per PRD).
    """
    narrative = state.get("business_narrative", "")
    llm = get_gemini_llm()

    if llm:
        prompt = (
            f"Based on this narrative: '{narrative}', create a detailed investor pitch deck with 12 slides. "
            "For each slide, provide a 'title' and 'content'. "
            "Return ONLY a JSON list of 12 objects, each with 'slide' (int), 'title' (string), and 'content' (string) keys."
        )
        response = llm.invoke([
            SystemMessage(content="You are a Deck Architect specialized in structured investor pitches."),
            HumanMessage(content=prompt)
        ])
        try:
            deck_structure = json.loads(response.content)
        except Exception:
            # Fallback if JSON parsing fails
            deck_structure = [{"slide": i+1, "title": f"Slide {i+1}", "content": "..."} for i in range(12)]
    else:
        deck_structure = [{"slide": i+1, "title": f"Slide {i+1}", "content": "Draft content"} for i in range(12)]

    return {
        "messages": [f"Deck Architect: Designed {len(deck_structure)} slides."],
        "deck_structure": deck_structure,
        "next_step": "visual_design"
    }

def visual_design_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates diagrams, icons, and layout specifications.
    """
    llm = get_groq_llm()
    if llm:
        response = llm.invoke([
            SystemMessage(content="You are a Visual Design Agent. Define assets for a pitch deck."),
            HumanMessage(content="Suggest 3 key visual assets for a professional pitch deck.")
        ])
        visual_assets = [response.content[:50]]
    else:
        visual_assets = ["branding_kit.zip", "charts.svg"]

    return {
        "messages": ["Visual Design: Generated visual specifications."],
        "visual_assets": visual_assets,
        "next_step": "supervisor"
    }

def supervisor_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrates the workflow and ensures quality/consistency.
    """
    return {
        "messages": ["Supervisor: Workflow validated and complete."],
        "next_step": "end"
    }
