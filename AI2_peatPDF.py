import fitz
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re

network_node_folder = 'C:\\Users\\prane\\PycharmProjects\\pythonProject8\\pythonProject11\\'
network_node_filename = 'AI2Peat_List.csv'
Download_PDF = '//div[@class="full-text"]/ul/li/a'
abstract_filename = "Abstract.csv"
List_PDFName = []

AI2peat_DF = pd.read_csv(network_node_folder+network_node_filename, sep=';')
Arxiv = 'Paper_Link'
ArxivPaperNumber = 'Paper_Number'

abstract_columns = ['Paper_Number', 'Abstract']
abstract_df = pd.DataFrame(columns=abstract_columns)
abstract_df.to_csv(abstract_filename, sep=';', index=False)

rows_with_arxiv = AI2peat_DF[AI2peat_DF[Arxiv].str.contains('arxiv.org', case=False, na=False)]


Arxiv_List = rows_with_arxiv[Arxiv].tolist()
Arxiv_List2 = rows_with_arxiv[ArxivPaperNumber].tolist()


# Print the list of values
print(f'{Arxiv_List=}')
print(f'{Arxiv_List2=}')
# def get_content(doc, heading_name) :
    #seek(doc, heading_name)
    # extract the content
    # decide/determine when the content ends

# def seek(doc, heading_name) :
    # go through the paper and return the point in which heading_name is found

# def update_references(content) :
    # update AI2Peat_Relationship.csv

# def update_abstracts(content) :
    # do something with it

def driver_init():
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": network_node_folder}

    options.add_experimental_option("prefs", {"download.prompt_for_download": False,
                                                     "plugins.always_open_pdf_externally": True})
    options.add_experimental_option("prefs", prefs)  # Corrected line
    options.add_experimental_option("prefs", {"download.prompt_for_download": False,
                                              "plugins.always_open_pdf_externally": True,
                                              "download.default_directory": network_node_folder})
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get(SearchSite)
    driver.implicitly_wait(0.5)
    return driver

def download_init(driver):
    DownloadButtom = driver.find_element(By.XPATH, Download_PDF)
    PDFName = DownloadButtom.get_attribute('href')
    List_PDFName.append(PDFName)



    DownloadButtom.click()
    time.sleep(10)

    driver.close()

def extract_abstract(pdf_path):
    pdf_document = fitz.open(pdf_path)

    abstract = ""

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text()
        #get_blocks -PyMuPDF
        #NEed to find a way to store the abstract and to link them with the paper, same for references.
        #Find a way to download the paper automatically, start with Archivex.


        abstract_match = re.search(r'\nAbstract\n[:\s]*([\s\S]*?)(\.\s*\nIntroduction|$)', text, re.IGNORECASE)

        if abstract_match:
            abstract += abstract_match.group(1)

    pdf_document.close()

    print(f'the abstract for {pdf_path} is:')
    print(abstract)
    print('-------')

    return abstract

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

def abstract_writting(Paper_Number, pdf_local_filename):
    abstract_text = extract_abstract(network_node_folder + pdf_local_filename)
    abstract_text = abstract_text.replace('-\n', '')
    abstract_text = abstract_text.replace('\n', ' ')

    abstract_df = pd.read_csv(abstract_filename, sep=';')

    new_row = pd.DataFrame([[Paper_Number, abstract_text]],
                           columns=abstract_df.columns)
    abstract_df = pd.concat([abstract_df, new_row], ignore_index=True)

    abstract_df.to_csv(abstract_filename, sep=';', index=False)






for i in range(len(Arxiv_List)):
    SearchSite = Arxiv_List[i]
    download_init(driver_init())

List_PDFName = [s.split('https://arxiv.org/pdf/')[-1] for s in List_PDFName if 'https://arxiv.org/pdf/' in s]
print(f'{List_PDFName=}')

# zip is the same as:
# pythonchallenge.com
#for i in range(len(Arxiv_List2)) :
#    pdf_name = Arxiv_List2[í]
#    pdf_local_filename = List_PDFName[í]

for paper_number, pdf_local_filename in zip(Arxiv_List2, List_PDFName) :
    print(f'gonna call abstract_writting passing {paper_number=} {pdf_local_filename=}')
    abstract_writting(paper_number, pdf_local_filename)