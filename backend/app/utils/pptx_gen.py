from pptx import Presentation
from pptx.util import Inches, Pt
import io
from typing import List, Dict, Any

def generate_pptx(slides_data: List[Dict[str, Any]]) -> io.BytesIO:
    """
    Generates a PowerPoint presentation from the provided slide data.
    """
    prs = Presentation()

    for slide_data in slides_data:
        title_str = slide_data.get("title", f"Slide {slide_data.get('slide', '')}")
        content_str = slide_data.get("content", "")

        # Use the title and content layout
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        title = slide.shapes.title
        content = slide.placeholders[1]

        title.text = title_str
        content.text = content_str

    pptx_io = io.BytesIO()
    prs.save(pptx_io)
    pptx_io.seek(0)
    return pptx_io
