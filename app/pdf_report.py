from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_pdf_report(
    report_text,
    output_path="reports/emotion_report.pdf"
):

    # 한글 폰트 등록
    pdfmetrics.registerFont(
        TTFont(
            "Malgun",
            "C:/Windows/Fonts/malgun.ttf"
        )
    )

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    body_style = styles["BodyText"]

    title_style.fontName = "Malgun"
    body_style.fontName = "Malgun"

    content = []

    title = Paragraph(
        "마음동행 AI 감정 분석 보고서",
        title_style
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    report = Paragraph(
        report_text.replace("\n", "<br/>"),
        body_style
    )

    content.append(report)

    doc.build(content)

    return output_path

