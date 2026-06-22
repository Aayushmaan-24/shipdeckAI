from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import io
from typing import List, Dict, Any

def generate_pptx(slides_data: List[Dict[str, Any]]) -> io.BytesIO:
    """
    Generates a PowerPoint presentation with a dark-themed, modern design.
    """
    prs = Presentation()

    # Set 16:9 aspect ratio
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    # Colors
    BG_COLOR = RGBColor(2, 6, 23)      # slate-950
    ACCENT_COLOR = RGBColor(37, 99, 235) # blue-600
    TEXT_MAIN = RGBColor(255, 255, 255) # white
    TEXT_DIM = RGBColor(203, 213, 225)  # slate-300

    for i, slide_data in enumerate(slides_data):
        # Restore fallback for title
        title_str = slide_data.get("title") or f"Slide {i+1}"
        content_str = slide_data.get("content", "")

        # Use a blank layout for maximum control
        slide_layout = prs.slide_layouts[6]
        slide = prs.slides.add_slide(slide_layout)

        # 1. Background
        background = slide.shapes.add_shape(
            1, # Rectangle
            0, 0, prs.slide_width, prs.slide_height
        )
        background.fill.solid()
        background.fill.fore_color.rgb = BG_COLOR
        background.line.no_fill = True # No border

        # 2. Accent Bar at the bottom
        accent_bar = slide.shapes.add_shape(
            1, # Rectangle
            0, prs.slide_height - Inches(0.1), prs.slide_width, Inches(0.1)
        )
        accent_bar.fill.solid()
        accent_bar.fill.fore_color.rgb = ACCENT_COLOR
        accent_bar.line.no_fill = True

        if i == 0:
            # Title Slide Layout
            # Main Title
            title_box = slide.shapes.add_textbox(
                0, prs.slide_height / 2 - Inches(1.2), prs.slide_width, Inches(1.5)
            )
            title_frame = title_box.text_frame
            title_frame.word_wrap = True

            p = title_frame.paragraphs[0]
            p.text = title_str
            p.font.size = Pt(48)
            p.font.bold = True
            p.font.color.rgb = TEXT_MAIN
            p.alignment = PP_ALIGN.CENTER

            # Subtitle / Content on Title Slide
            if content_str:
                subtitle_box = slide.shapes.add_textbox(
                    0, prs.slide_height / 2 + Inches(0.5), prs.slide_width, Inches(1)
                )
                subtitle_frame = subtitle_box.text_frame
                subtitle_frame.word_wrap = True
                p_sub = subtitle_frame.paragraphs[0]
                p_sub.text = content_str
                p_sub.font.size = Pt(24)
                p_sub.font.color.rgb = TEXT_DIM
                p_sub.alignment = PP_ALIGN.CENTER
        else:
            # Content Slide Layout
            # Title
            title_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(0.4), prs.slide_width - Inches(1), Inches(1)
            )
            title_frame = title_box.text_frame
            title_frame.word_wrap = True

            p = title_frame.paragraphs[0]
            p.text = title_str
            p.font.size = Pt(32)
            p.font.bold = True
            p.font.color.rgb = TEXT_MAIN
            p.alignment = PP_ALIGN.LEFT

            # Content
            content_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(1.5), prs.slide_width - Inches(1), prs.slide_height - Inches(2)
            )
            content_frame = content_box.text_frame
            content_frame.word_wrap = True

            lines = content_str.split('\n')
            for j, line in enumerate(lines):
                line_text = line.strip()
                if not line_text and j > 0: continue # Skip empty lines except possibly first

                if j == 0:
                    p = content_frame.paragraphs[0]
                else:
                    p = content_frame.add_paragraph()

                # Basic bullet indentation logic
                if line_text.startswith(('-', '*', '•')):
                    p.level = 1
                    p.text = line_text[1:].strip()
                else:
                    p.level = 0
                    p.text = line_text

                p.font.size = Pt(18)
                p.font.color.rgb = TEXT_DIM
                p.alignment = PP_ALIGN.LEFT

    pptx_io = io.BytesIO()
    prs.save(pptx_io)
    pptx_io.seek(0)
    return pptx_io
