from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: Annotated[List[str], lambda x, y: x + y]
    repo_path: str
    code_summary: str
    business_narrative: str
    deck_structure: List[dict]
    visual_assets: List[str]
    next_step: str

def repo_explorer_agent(state: AgentState):
    print("--- REPO EXPLORER AGENT ---")
    return {"messages": ["Explored repository structure."], "next_step": "code_intelligence"}

def code_intelligence_agent(state: AgentState):
    print("--- CODE INTELLIGENCE AGENT ---")
    return {"messages": ["Analyzed code logic and features."], "next_step": "business_strategist"}

def business_strategist_agent(state: AgentState):
    print("--- BUSINESS STRATEGIST AGENT ---")
    return {"messages": ["Synthesized business value proposition."], "next_step": "deck_architect"}

def deck_architect_agent(state: AgentState):
    print("--- DECK ARCHITECT AGENT ---")
    return {"messages": ["Designed slide deck structure."], "next_step": "visual_design"}

def visual_design_agent(state: AgentState):
    print("--- VISUAL DESIGN AGENT ---")
    return {"messages": ["Generated visual assets."], "next_step": "supervisor"}

def supervisor_agent(state: AgentState):
    print("--- SUPERVISOR AGENT ---")
    return {"messages": ["Orchestrating workflow."], "next_step": "end"}

def should_continue(state: AgentState):
    return state["next_step"]

workflow = StateGraph(AgentState)

workflow.add_node("repo_explorer", repo_explorer_agent)
workflow.add_node("code_intelligence", code_intelligence_agent)
workflow.add_node("business_strategist", business_strategist_agent)
workflow.add_node("deck_architect", deck_architect_agent)
workflow.add_node("visual_design", visual_design_agent)
workflow.add_node("supervisor", supervisor_agent)

workflow.set_entry_point("repo_explorer")

workflow.add_edge("repo_explorer", "code_intelligence")
workflow.add_edge("code_intelligence", "business_strategist")
workflow.add_edge("business_strategist", "deck_architect")
workflow.add_edge("deck_architect", "visual_design")
workflow.add_edge("visual_design", "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    should_continue,
    {
        "repo_explorer": "repo_explorer",
        "code_intelligence": "code_intelligence",
        "business_strategist": "business_strategist",
        "deck_architect": "deck_architect",
        "visual_design": "visual_design",
        "end": END
    }
)

app = workflow.compile()
