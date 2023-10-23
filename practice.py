import os
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import fitz  # Import fitz for PDF parsing

# Define constants as variables
CSV_FILE_PATH = 'AI2Peat_List.csv'
RELATIONSHIP_FILE_PATH = 'AI2Peat_Relationship.csv'
CHROME_DRIVER_PATH = r"C:\\Users\\prane\\PycharmProjects\\pythonProject8\\pythonProject11"
GOOGLE_SCHOLAR_URL = "https://scholar.google.com/"
SEARCH_QUERY = "Playing atari with deep reinforcement learning"
PDF_FILE_PATH = r'C:\\Users\\prane\\PycharmProjects\\pythonProject8\\pythonProject11'  # Update with your PDF path


def initialize_csv_files():
    # Initialize CSV files if they don't exist
    if not os.path.exists(CSV_FILE_PATH):
        initial_df = pd.DataFrame(columns=['Paper_Number', 'Paper_ID', 'Paper_Name', 'Paper_Link'])
        initial_df.to_csv(CSV_FILE_PATH, index=False, encoding='utf-8')

    if not os.path.exists(RELATIONSHIP_FILE_PATH):
        rel_df = pd.DataFrame(
            columns=['Paper_Number_Cited', 'Paper_Number_Quoter', 'Paper_Name_Cited', 'Paper_Name_Quoter'])
        rel_df.to_csv(RELATIONSHIP_FILE_PATH, index=False, encoding='utf-8')


def parse_pdf_references(pdf_file_path):
    references_section = ""
    is_references = False

    pdf_document = fitz.open(pdf_file_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        page_text = page.get_text()

        if "References" in page_text:
            is_references = True

        if is_references:
            references_section += page_text

    pdf_document.close()

    return references_section


def scrape_google_scholar(start_node_number=0):
    driver = start_web_driver()
    search_and_scrape(driver, start_node_number)
    driver.quit()


def start_web_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_DRIVER_PATH
    driver = webdriver.Chrome(options=options)
    driver.get(GOOGLE_SCHOLAR_URL)
    driver.implicitly_wait(0.5)
    return driver


def search_and_scrape(driver, start_node_number):
    search_for_query(driver)
    search_button = driver.find_element(By.ID, "gs_hdr_tsb")
    search_button.click()
    scrape_cited_by_pages(driver, start_node_number)


def search_for_query(driver):
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(SEARCH_QUERY)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(30)


def scrape_cited_by_pages(driver, start_node_number):
    citation_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Cited by")
    pages_list = citation_button.text
    pages_split = pages_list.split()
    number_pages = math.ceil(int(pages_split[-1]) / 10)
    citation_button.click()

    for page_next in range(number_pages):
        titles = driver.find_elements(By.XPATH, '//div[@class="gs_ri"]/h3/a')
        start_node_number = scrape_and_store_cited_results(driver, titles, start_node_number)
        click_next_page(driver)
        time.sleep(2)


def scrape_and_store_cited_results(driver, titles, start_node_number):
    rows_list = []
    for title in titles:
        original_index = str(start_node_number)
        row = [original_index, title.get_attribute("id"), title.text, title.get_attribute("href")]
        rows_list.append(row)
        start_node_number += 1
    new_df = pd.DataFrame(rows_list, columns=['Paper_Number', 'Paper_ID', 'Paper_Name', 'Paper_Link'])
    new_df.to_csv(CSV_FILE_PATH, mode='a', index=False, header=False, encoding='utf-8')
    return start_node_number


def click_next_page(driver, max_retries=5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            next_page = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@class="gs_btnPR gs_in_ib gs_btn_lrge gs_btn_half gs_btn_lsu"]'))
            )
            next_page.click()
            return  # Exit the loop if the click is successful
        except Exception as e:
            print("Failed to click the 'Next' button. Retrying...")
            retry_count += 1

    print("Max retries reached. Exiting loop.")


if __name__ == '__main__':
    initialize_csv_files()

    # Parse PDF references
    references_text = parse_pdf_references(PDF_FILE_PATH)
    print(references_text)  # You can print or process the references as needed

    # Specify the starting node number (0 is the default)
    scrape_google_scholar(start_node_number=10)