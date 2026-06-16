import pytest
from unittest.mock import patch, MagicMock
from backend.app.agents.workflow import app as workflow_app

@patch("backend.app.agents.logic.get_groq_llm")
@patch("backend.app.agents.logic.get_gemini_llm")
def test_workflow_execution(mock_gemini, mock_groq):
    # Mock LLMs
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Mocked content"
    mock_llm.invoke.return_value = mock_response

    # For structured output in gemini
    mock_structured_llm = MagicMock()
    mock_pitch_deck = MagicMock()
    mock_slide = MagicMock()
    mock_slide.dict.return_value = {"slide": 1, "title": "Title", "content": "Content"}
    mock_pitch_deck.slides = [mock_slide] * 12
    mock_structured_llm.invoke.return_value = mock_pitch_deck

    mock_groq.return_value = mock_llm
    mock_gemini.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm

    initial_state = {
        "messages": ["Start"],
        "repo_path": "https://github.com/test/repo",
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
