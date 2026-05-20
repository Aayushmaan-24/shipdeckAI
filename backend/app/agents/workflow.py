from typing import List, TypedDict, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
from backend.app.agents.logic import (
    repo_explorer_agent,
    code_intelligence_agent,
    business_strategist_agent,
    deck_architect_agent,
    visual_design_agent,
    supervisor_agent
)

class AgentState(TypedDict):
    messages: Annotated[List[str], lambda x, y: x + y]
    repo_path: str
    code_summary: str
    business_narrative: str
    deck_structure: List[Dict[str, Any]]
    visual_assets: List[str]
    next_step: str

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
