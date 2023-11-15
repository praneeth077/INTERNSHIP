import fitz  # PyMuPDF
import re


def extract_abstract(pdf_path):
    pdf_document = fitz.open(pdf_path)

    abstract = ""

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text()

        # Customize the regex pattern based on the structure of your PDFs
        abstract_match = re.search(r'Abstract[:\s]*([\s\S]*?)(\.\s*\n|$)', text, re.IGNORECASE)

        if abstract_match:
            abstract += abstract_match.group(1)

    pdf_document.close()

    return abstract


# Example usage
pdf_path = 'C:\\Users\\prane\\PycharmProjects\\pythonProject8\\pythonProject11\\arxiv.pdf'
abstract_text = extract_abstract(pdf_path)
print(abstract_text)
def extract_references(pdf_path):
    pdf_document = fitz.open(pdf_path)
    references = ""
    references_started = False

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text()

        # Check if "References" is found in the text
        references_match = re.search(r'\nReferences[:\s*\n|$)]*([\s\S]*)$', text, re.IGNORECASE)

        if references_match:
            references += references_match.group(1)
            references_started = True
            continue  # Skip the current page with the "References" heading

        # If references_started is True, append the text
        if references_started:
            references += text

    pdf_document.close()

    return references


# Example usage
pdf_path = 'C:\\Users\\prane\\PycharmProjects\\pythonProject8\\pythonProject11\\arxiv.pdf'
references_text = extract_references(pdf_path)
print("============================================")
print(references_text)