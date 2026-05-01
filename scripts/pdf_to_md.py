"""Convert PDF to Markdown using pypdf."""
import sys
from pathlib import Path

from pypdf import PdfReader


def pdf_to_markdown(pdf_path: str, md_path: str | None = None) -> str:
    reader = PdfReader(pdf_path)
    lines: list[str] = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        if i > 0:
            lines.append("\n---\n")
        lines.append(text.strip())

    md_content = "\n\n".join(lines)

    if md_path:
        Path(md_path).write_text(md_content, encoding="utf-8")
        print(f"Written to {md_path}")

    return md_content


if __name__ == "__main__":
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "data/和豆包的对话_0501.pdf"
    md_file = sys.argv[2] if len(sys.argv) > 2 else pdf_file.replace(".pdf", ".md")
    pdf_to_markdown(pdf_file, md_file)
