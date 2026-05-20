import pytest
from backend.app.agents.workflow import app as workflow_app

def test_workflow_execution():
    initial_state = {
        "messages": ["Start"],
        "repo_path": "test_repo",
        "code_summary": "",
        "business_narrative": "",
        "deck_structure": [],
        "visual_assets": [],
        "next_step": ""
    }

    # Use invoke for testing; it will use mocked logic since API keys are missing
    result = workflow_app.invoke(initial_state)

    assert "messages" in result
    assert result["next_step"] == "end"
    assert len(result["deck_structure"]) > 0
