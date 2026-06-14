from pypdf import PdfReader


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

<<<<<<< HEAD
    clean_text=" ".join(text.split())
    return clean_text   
=======
    return text
>>>>>>> bd4bee68d969567e2f8361cb6009350dbeb23d00
