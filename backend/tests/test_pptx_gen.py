import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from backend.app.utils.pptx_gen import generate_pptx

def test_generate_pptx_properties():
    slides_data = [
        {"slide": 1, "title": "Main Title", "content": "Welcome to ShipDeck Subtitle"},
        {"slide": 2, "title": "Features", "content": "- Feature 1\n- Feature 2"},
        {"slide": 3, "content": "Slide without title"}
    ]

    pptx_io = generate_pptx(slides_data)
    prs = Presentation(pptx_io)

    # Verify dimensions (16:9)
    assert prs.slide_width == Inches(10)
    assert prs.slide_height == Inches(5.625)

    # Verify slide count
    assert len(prs.slides) == 3

    # Colors to verify
    BG_COLOR_EXPECTED = RGBColor(2, 6, 23)
    ACCENT_COLOR_EXPECTED = RGBColor(37, 99, 235)
    TEXT_MAIN_EXPECTED = RGBColor(255, 255, 255)
    TEXT_DIM_EXPECTED = RGBColor(203, 213, 225)

    for i, slide in enumerate(prs.slides):
        # 1. Check background rectangle
        bg_rect = slide.shapes[0]
        assert bg_rect.fill.fore_color.rgb == BG_COLOR_EXPECTED
        assert bg_rect.line.fill.type is None or bg_rect.line.fill.type == 0 # no fill

        # 2. Check accent bar
        accent_bar = slide.shapes[1]
        assert accent_bar.fill.fore_color.rgb == ACCENT_COLOR_EXPECTED

        if i == 0:
            # Title slide
            title_box = slide.shapes[2]
            title_frame = title_box.text_frame
            assert title_frame.word_wrap is True

            p = title_frame.paragraphs[0]
            assert p.text == "Main Title"
            assert p.font.size == Pt(48)
            assert p.font.color.rgb == TEXT_MAIN_EXPECTED

            # Subtitle
            subtitle_box = slide.shapes[3]
            assert subtitle_box.text_frame.paragraphs[0].text == "Welcome to ShipDeck Subtitle"
            assert subtitle_box.text_frame.paragraphs[0].font.size == Pt(24)
        elif i == 1:
            # Content slide
            title_box = slide.shapes[2]
            assert title_box.text_frame.paragraphs[0].text == "Features"
            assert title_box.text_frame.paragraphs[0].font.size == Pt(32)
            assert title_box.text_frame.paragraphs[0].font.color.rgb == TEXT_MAIN_EXPECTED

            content_box = slide.shapes[3]
            content_frame = content_box.text_frame
            assert content_frame.word_wrap is True
            assert len(content_frame.paragraphs) == 2
            assert content_frame.paragraphs[0].font.size == Pt(18)
            assert content_frame.paragraphs[0].font.color.rgb == TEXT_DIM_EXPECTED
            assert content_frame.paragraphs[0].level == 1
        elif i == 2:
            # Fallback title
            title_box = slide.shapes[2]
            assert title_box.text_frame.paragraphs[0].text == "Slide 3"

if __name__ == "__main__":
    test_generate_pptx_properties()
    print("PPTX Generation tests passed!")
