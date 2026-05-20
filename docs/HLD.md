# ShipDeck High-Level Design (HLD)

## Architecture Overview
ShipDeck follows a modern multi-agent architecture designed for scalability and extensibility using free-tier AI models.

### Components
1. **Frontend**: Next.js 15 (App Router) + TypeScript + Tailwind CSS.
2. **Backend**: FastAPI + LangGraph.
3. **Agentic System**: Multi-agent orchestration powered by LangGraph.
4. **Storage**: Cloudflare R2 (ZIP/Deck storage) + Neon Postgres (Metadata).

## Multi-Agent Workflow
The system uses a series of specialized agents to process code and generate pitch decks:

- **Repo Explorer Agent**: Navigates and understands the repository structure.
- **Code Intelligence Agent**: Extracts technical stack, architecture, and core features.
- **Business Strategist Agent**: Synthesizes the value proposition and business narrative.
- **Deck Architect Agent**: Defines the structure and content of each slide (12-16 slides).
- **Visual Design Agent**: Generates diagrams, icons, and layout specifications.
- **Supervisor Agent**: Orchestrates the workflow and ensures quality/consistency.

## Tech Stack (v1.0)
- **Inference**: Groq (Llama 3.3 70B), Hugging Face, Gemini Flash (Free).
- **Workflow**: LangGraph / LangChain.
- **Database**: Neon (Postgres).
- **Deployment**: Vercel (Frontend), Railway/Render (Backend).
