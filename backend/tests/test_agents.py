import pytest
from unittest.mock import MagicMock, patch
from backend.app.agents.logic import repo_explorer_agent, code_intelligence_agent, business_strategist_agent

@patch("backend.app.agents.logic.get_groq_llm")
def test_repo_explorer_agent_with_mock_llm(mock_get_llm):
    # Mock LLM response
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "LLM analyzed repo"
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm

    state = {"repo_path": "https://github.com/user/repo", "messages": []}
    result = repo_explorer_agent(state)
    assert "LLM analyzed repo" in result["messages"][0]

@patch("backend.app.agents.logic.get_groq_llm")
def test_code_intelligence_agent_mock(mock_get_llm):
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Stack: Mocked"
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm

    state = {"messages": ["Repo Explorer: some summary"]}
    result = code_intelligence_agent(state)
    assert result["next_step"] == "business_strategist"

@patch("backend.app.agents.logic.get_groq_llm")
def test_business_strategist_agent_mock(mock_get_llm):
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Mocked Narrative"
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm

    state = {"code_summary": "Test Stack"}
    result = business_strategist_agent(state)
    assert result["next_step"] == "deck_architect"
