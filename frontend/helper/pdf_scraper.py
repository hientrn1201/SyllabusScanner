from pypdf import PdfReader


def scrape(file):
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()
    return text
