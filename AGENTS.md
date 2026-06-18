# ShipDeck Agent Instructions

This document provides instructions and guidelines for AI agents working on the ShipDeck codebase.

## 🤖 AI Models & APIs

- **Strict Constraint:** Use ONLY free-tier AI models and APIs for v1.0.
  - Primary Inference: Groq (Llama 3.3 70B)
  - Structured Generation: Google Gemini 1.5 Flash (Free Tier)
- Ensure all LLM calls handle missing API keys gracefully by checking environment variables before instantiation.

## 🏗 Architectural Patterns

- **Multi-Agent Workflow:** Orchestrated using LangGraph. Agents are defined as functions in `backend/app/agents/logic.py` and connected in `backend/app/agents/workflow.py`.
- **Structured Outputs:** Use Pydantic V2 for structured data. Always use `.model_dump()` instead of the deprecated `.dict()` method for serialization.
- **Streaming Response:** The generation process MUST support real-time streaming to the frontend using FastAPI's `StreamingResponse` and SSE (Server-Sent Events).

## 💻 Backend Conventions

- **Internal Imports:** Use the `backend.app` prefix for all internal imports (e.g., `from backend.app.agents.logic import ...`).
- **Path Handling:** Execute backend commands from the repository root with `PYTHONPATH=.`.
- **Validation:** Strict validation for GitHub URLs is required (must start with `https://github.com/`).

## 🎨 Frontend Conventions

- **Next.js 15 & React 19:** Follow the latest patterns for Next.js 15 (App Router) and React 19.
- **Styling:** Use Tailwind CSS with PostCSS. Ensure `postcss.config.js` includes `tailwindcss` and `autoprefixer`.
- **SSE Handling:** The frontend must robustly handle SSE streams, including malformed JSON and connection interruptions.
