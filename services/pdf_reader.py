from pypdf import PdfReader
from services.text_processor import save_documnet_to_db

def extract_pages(pdf_file):

    reader = PdfReader(pdf_file)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text:

            pages.append(
                {
                    "page": page_number,
                    "text": text
                }
            )

    return pages 

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    clean_text=" ".join(text.split())
    if hasattr(pdf_file,'name'):
        save_documnet_to_db(pdf_file.name,clean_text)
    else:
        save_documnet_to_db("uploaded_document.pdf",clean_text)
    return clean_text        

