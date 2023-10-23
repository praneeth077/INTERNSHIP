import fitz


file_path = 'C:\\Users\\prane\\PycharmProjects\\pythonProject8\\pythonProject11\\'

pdf_document = fitz.open(file_path)


references_section = ""
is_references = False


for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    page_text = page.get_text()


    if "References" in page_text:
        is_references = True


    if is_references:
        references_section += page_text


pdf_document.close()


print(references_section)