# ShipDeck 🚢

**ShipDeck** is an AI-powered platform that transforms GitHub repositories into investor-grade pitch decks in minutes. By orchestrating a multi-agent system, ShipDeck analyzes your codebase, identifies technical strengths, synthesizes a compelling business narrative, and generates a professional PowerPoint presentation.

## 🚀 Features

- **Automated Repository Intelligence:** Deep analysis of tech stack, architecture, and core features using the GitHub API.
- **Business Strategy Engine:** AI-driven synthesis of value propositions, problem statements, and target audiences.
- **Multi-Agent Orchestration:** Powered by **LangGraph**, specialized agents work together (Explorer, Architect, Strategist, Supervisor) to craft your deck.
- **Real-Time Generation Dashboard:** Watch the agents work in real-time with a live execution log and progress tracking.
- **Professional PPTX Export:** Download high-quality, 16:9 dark-themed PowerPoint presentations ready for investor meetings.
- **Responsive Modern UI:** A sleek, high-performance interface built with Next.js 15 and Framer Motion.

## 🛠 Tech Stack

### Frontend
- **Framework:** [Next.js 15](https://nextjs.org/) (App Router)
- **Library:** [React 19](https://react.dev/)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **Components:** [Shadcn UI](https://ui.shadcn.com/)
- **Animations:** [Framer Motion](https://www.framer.com/motion/)
- **Icons:** [Lucide React](https://lucide.dev/)

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **AI Orchestration:** [LangGraph](https://www.langchain.com/langgraph), [LangChain](https://www.langchain.com/)
- **PowerPoint Generation:** [python-pptx](https://python-pptx.readthedocs.io/)
- **Streaming:** Server-Sent Events (SSE) for real-time updates.

### AI Models
- **Primary Inference:** [Groq](https://groq.com/) (Llama 3.3 70B)
- **Structured Generation:** [Google Gemini 1.5 Flash](https://aistudio.google.com/)

## 🏗 Architecture

ShipDeck utilizes a modular, agentic architecture:
1.  **Repo Explorer:** Fetches metadata and file structures from GitHub.
2.  **Code Intelligence:** Analyzes the technical stack and architectural patterns.
3.  **Business Strategist:** Frames the project within a market context and defines the "why".
4.  **Deck Architect:** Structures the 12-16 slides with professional content.
5.  **Supervisor:** Performs final quality checks and ensures data consistency.

## 📁 Folder Structure

```text
shipdeck/
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── agents/         # LangGraph agents and workflow
│   │   ├── api/            # API endpoints (health, generate, download)
│   │   ├── utils/          # PPTX generation utilities
│   │   └── main.py         # Entry point
│   ├── tests/              # Backend test suite
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js application
│   ├── app/                # Pages and layouts
│   ├── components/         # UI components
│   ├── lib/                # Utilities and types
│   └── package.json        # Node.js dependencies
└── README.md               # You are here
```

## ⚙️ Installation & Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Groq API Key](https://console.groq.com/)
- [Google AI Studio API Key](https://aistudio.google.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/Aayushmaan-24/shipdeckAI.git
cd shipdeckAI
```

### 2. Backend Setup
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Configure environment variables
# Create a .env file in the root directory
echo "GROQ_API_KEY=your_key_here" >> .env
echo "GOOGLE_API_KEY=your_key_here" >> .env

# Start the server
PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
# Install dependencies (use legacy-peer-deps for React 19 RC compatibility)
npm install --legacy-peer-deps

# Start development server
npm run dev
```
Visit `http://localhost:3000` to start building.

## 🧪 Running Tests

### Backend Tests
```bash
PYTHONPATH=. pytest backend/tests/
```

### Frontend Linting
```bash
cd frontend
npm run lint
```

## 🗺 Roadmap & Limitations

### Current Limitations
- Supports public GitHub repositories only.
- Analysis is limited to the first 1000 files and partial README content.
- Generates text-based layouts (Architecture diagrams are simplified).

### Future Roadmap
- [ ] Support for private repositories via GitHub OAuth.
- [ ] AI-generated image/diagram generation for slides.
- [ ] Custom theme selection (Light mode, Brand colors).
- [ ] Export to PDF and Google Slides.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Built with 🚢 by the ShipDeck Team.
