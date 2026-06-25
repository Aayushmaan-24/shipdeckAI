import sys
import os
from io import BytesIO

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.utils.pptx_gen import generate_pptx

def test_generate_pptx_success():
    sample_slides = [
        {
            "title": "ShipDeck: Pitch Deck Generator",
            "content": "From code to deck in minutes.",
            "layout_type": "text"
        },
        {
            "title": "The Problem",
            "content": "- Writing pitch decks is slow\n- Developers hate PowerPoint\n- Consistency is hard to maintain",
            "layout_type": "text"
        },
        {
            "title": "Key Features",
            "content": "Automated Analysis\nMulti-Agent System\nModern Design\nPPTX Export\nCloud Integration\nFast Turnaround",
            "layout_type": "grid"
        },
        {
            "title": "Architecture",
            "content": "Frontend (Next.js)\nBackend (FastAPI)\nAgents (LangGraph)\nPowerPoint (python-pptx)",
            "layout_type": "architecture"
        }
    ]

    try:
        pptx_io = generate_pptx(sample_slides)
        assert isinstance(pptx_io, BytesIO)
        assert pptx_io.getbuffer().nbytes > 0
        print("PPTX generation test passed successfully!")
    except Exception as e:
        print(f"PPTX generation test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_generate_pptx_success()
