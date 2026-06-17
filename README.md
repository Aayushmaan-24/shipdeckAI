# ShipDeck 🚢

ShipDeck is an AI-powered platform that transforms GitHub repositories into investor-grade pitch decks in minutes.

## 🚀 Features

- **Automated Repo Analysis:** Extracts tech stack and key features directly from GitHub.
- **Business Storytelling:** Synthesizes a compelling narrative from technical capabilities.
- **Structured Pitch Decks:** Generates 12-16 professional slides using advanced AI agents.
- **Real-time Progress:** Watch the agents work through a streaming API.

## 🛠 Tech Stack

- **Frontend:** Next.js 15, React 19, Tailwind CSS
- **Backend:** FastAPI, LangGraph, LangChain
- **AI Models:** Groq (Llama 3.3 70B), Google Gemini 1.5 Flash (Free Tier)

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- [Groq API Key](https://console.groq.com/)
- [Google AI Studio API Key](https://aistudio.google.com/)

## ⚙️ Setup

### Backend

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```
3. Start the backend server (from the root directory):
   ```bash
   PYTHONPATH=. uvicorn backend.app.main:app --reload
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 🧪 Testing

Run the full test suite from the root directory:
```bash
PYTHONPATH=. python3 -m pytest backend/tests/
```

## 📄 License

This project is licensed under the MIT License.
