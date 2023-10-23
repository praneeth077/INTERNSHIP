import os
import math
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


#Constants turned into Variables
network_node_folder = 'C:\\Users\\prane\\PycharmProjects\\pythonProject8\\pythonProject11\\' 
network_node_filename = 'AI2Peat_List.csv'
network_edge_filename = 'AI2Peat_Relationship.csv'

citation_tag = {'por': 'Citado por', 'eng': 'Cited by'}
scraping_language = 'eng'
FirstSearch = "Playing atari with deep reinforcement learning"
Search = FirstSearch
SearchBarName = 'q'
TitleXPath = '//div[@class="gs_ri"]/h3/a'
NextButtonXPath = '//button[@class="gs_btnPR gs_in_ib gs_btn_lrge gs_btn_half gs_btn_lsu"]'
PaperNumber = 'Paper_Number'
PaperName = 'Paper_Name'
SearchSite = 'https://scholar.google.com/'
DriverPath = r"C:\Users\Pc\Desktop\Python Codes"

#initializing index variable
Index = 0
#Initializing Chrome Drivers
#os.environ['PATH'] += DriverPath


#This Part will look if there is already a CSV file named AI2Peat_List.csv created, if not it will create and go for the
#first search, otherwise it will search for the names contained in the CSV file

def init_files():
    with open(network_node_filename, 'w') as File:
        File.write('Paper_Number;Paper_ID;Paper_Name;Paper_Link' + '\n')
    with open(network_edge_filename, 'w') as File:
        File.write('Paper_Number_Cited;Paper_Number_Quoter' + '\n')

# In this part, the program will access the Google Scholar site.
def driver_init():
    driver = webdriver.Chrome()
    driver.get(SearchSite)
    driver.implicitly_wait(0.5)
    return driver
#Here it will acess the Search Bar and search for the first paper
def search_init():
    #global driver

    SearchBar = driver.find_element(By.NAME, SearchBarName)
    SearchBar.send_keys(Search)
    #time.sleep(5)

    SearchBar.send_keys(Keys.ENTER)

# Here it will find the Citations link. It extracts the number of papers from the link, then divides by 10, so we can now how many pages the
#program will need to through to get all the pages. After that it clicks on the link.
def scrapping():

    global Index

    CitationButton = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, citation_tag[scraping_language]))
    )
    PagesList = CitationButton.text
    PagesSplit = PagesList.split()
    NumberPages = math.ceil(int(PagesSplit[-1]) / 10)
    CitationButton.click()
#-----------------------------------------------------------------------

    #time.sleep(5)

#Here it will start the scrapping and write the data into both CSV files created.
    for PageNext in range(NumberPages):
        Titles = driver.find_elements(By.XPATH, TitleXPath)

        with open(network_node_filename, 'a', encoding='utf-8') as ListFile, open(network_edge_filename, 'a') as RelationshipFile:
            for i in range(len(Titles)):
                Index += 1
                encoded_text = Titles[i].text.encode('utf-8', 'ignore').decode('utf-8')
                ListFile.write(
                    f"{Index};{Titles[i].get_attribute('id')};{encoded_text} ;{Titles[i].get_attribute('href')}\n")

                RelationshipFile.write(
                    str(OriginalIndex) + ';' + str(Index) + '\n')
# If there isn't anymore pages to go through, this try/catch clause will finish the loop. It is needed, because even if the paper
# has thousands of citations, the google scholar has a limit of 100 pages.
        try:
                NextPage = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, NextButtonXPath ))
                )
                NextPage.click()
        except Exception as e:
            print("Failed to click the 'Next' button. Exiting loop.")
            break  # Exit the loop if clicking fails





if not os.path.exists(network_node_folder + network_node_filename):
    # write code to initialise the nodes and edges filenames



    init_files()
 #---------------------------------------------------------------------
# In this part, the program will acess the Google Scholar site.


    driver_init()
    driver = driver_init()
#--------------------------------------------------------------------
#Here it will acess the Search Bar and search for the first paper



    search_init()
    time.sleep(30)
#-------------------------------------------------------------------
# Now it will find the name of the first paper by the XPath and then write it on the CSV file and then click on the paper.
    Index = 0
    OriginalTitle = driver.find_element(By.XPATH, TitleXPath)
    OriginalName = OriginalTitle.text

 #-----------------------------------------------------------------
# Here we are opening the CSV file and writing the data from the first paper
    with open(network_node_filename, 'a', encoding='utf-8') as File:
        File.write(str(Index) + ';' + OriginalTitle.get_attribute('id') + ';' + OriginalTitle.text + ';' + OriginalTitle.get_attribute('href') + '\n')
    OriginalIndex = Index




# --------------------------------------------------------------------
# Here it will find the Citations link. It extracts the number of papers from the link, then divides by 10, so we can now how many pages the
#program will need to through to get all the pages. After that it clicks on the link.

    scrapping()
#--------------------------------------------------------------------
#This will start only if the CSV file, named AI2Peat_List has already been created.
else:
    # Read the CSV file to get the Paper_Name for Paper_ID = 1
    df = pd.read_csv(network_node_filename, delimiter=';')



#In this part it will start getting the data from the other papers. If the data in contained in the column is equal to the first paper we searched or it is the title of the column,
        # it will instead pass and continue the loop
    DontSearchAgainList = [FirstSearch]

    with open(network_node_filename, 'r') as csv_file:

        csv_file = open(network_node_filename, 'r', encoding='utf-8')
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        # Initialize a variable to store the last row
        lastRow = None

        # Iterate through the rows and store the last row
        for row in csv_reader:
            lastRow = row

        # Access the value in the first column of the last row
        if lastRow:
            NumberLoops = int(lastRow[PaperNumber])
            Index = NumberLoops

        csv_file.seek(0)

        for i2 in range(NumberLoops):


            for row in csv_reader:

                random_row = df.sample(n=1).iloc[0]
                Search = random_row['Paper_Name']

                if Search in DontSearchAgainList or Search == (PaperName):
                    pass
                # ----------------------------------------------------------
                # Here is where the code will open the Chrome browser again and it will get the name of the paper from the CSV and search for it
                else:

                    driver_init()
                    driver = driver_init()

                    search_init()

                    time.sleep(30)

                    OriginalIndex = random_row['Paper_Number']
                    # ---------------------------------------------------
                    # Here it will find the Citations link. It extracts the number of papers from the link, then divides by 10, so we can now how many pages the
                    # program will need to through to get all the pages. After that it clicks on the link. If the paper isn't cited by any other, it will close the window and the loop, and continue
                    # searching for toher papers

                    try:
                        CitationButton = driver.find_element(By.PARTIAL_LINK_TEXT, citation_tag[scraping_language])
                        PagesList = CitationButton.text
                        PagesSplit = PagesList.split()
                        NumberPages = math.ceil(int(PagesSplit[-1]) / 10)

                        CitationButton.click()
                    except Exception as e:

                        driver.close()  # Close the webpage window
                        continue
                        # time.sleep(5)
                    time.sleep(30)
                    # ------------------------------------------------------------------------
                    # Here it will start the scrapping and write the data into both CSV files created.
                    for PageNext in range(NumberPages):
                        Titles = driver.find_elements(By.XPATH, TitleXPath)

                        with open(network_node_filename, 'a', encoding='utf-8') as ListFile, open(network_edge_filename, 'a', encoding='utf-8') as RelationshipFile:

                            for i in range(len(Titles)):
                                Index += 1
                                ListFile.write(f"{Index};{Titles[i].get_attribute('id')};{Titles[i].text.encode('utf-8', 'ignore').decode('utf-8')} ;{Titles[i].get_attribute('href')}\n")

                                RelationshipFile.write(
                                    str(OriginalIndex) + ';' + str(Index) + '\n')
                        # -----------------------------------------------------------------
                        # If there isn't anymore pages to go through, this try/catch clause will finish the loop. It is needed, because even if the paper
                        # has thousands of citations, the google scholar has a limit of 100 pages.
                        try:
                            NextPage = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH,
                                     NextButtonXPath))
                            )
                            NextPage.click()
                        except Exception as e:

                            driver.close()  # Close the webpage window
                            continue  # Continue the loop