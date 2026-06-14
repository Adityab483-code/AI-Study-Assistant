from pypdf import PdfReader


def extract_text(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    clean_text=" ".join(text.split())
    return clean_text   