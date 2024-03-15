from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# Set logging level to suppress specific logs
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('selenium').setLevel(logging.ERROR)
options = Options()
options.add_argument('--headless')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')

import os

# Get the current working directory
current_directory = os.getcwd()
from urllib.parse import urlparse, parse_qs
from openpyxl import Workbook
import os

# Initialize workbook and worksheet
wb = Workbook()
ws = wb.active
def extract_sku_from_url(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Get the path from the parsed URL
    path = parsed_url.path
    
    # Split the path by '/'
    path_parts = path.split('/')
    
    # Find the index of 'dp' in the path
    dp_index = path_parts.index('dp') if 'dp' in path_parts else -1
    
    # If 'dp' is found, return the next part as SKU
    if dp_index != -1 and dp_index < len(path_parts) - 1:
        return path_parts[dp_index + 1]
    else:
        # If 'dp' is not found or if there are no parts after 'dp', try to extract the SKU from query parameters
        query_params = parse_qs(parsed_url.query)
        if 'url' in query_params:
            url_param = query_params['url'][0]
            return extract_sku_from_url(url_param)
        else:
            return None
def link_scrape(url):
    try:
    # Try to install and use the latest version of Chrome WebDriver
        driver = webdriver.Chrome(options=options)
    except:
        # If the latest version is not available, use the previous version
        driver = webdriver.Chrome(options=options)



    driver.get(url)
    xlsx_filename = 'SKU_files/sku.xlsx'

    # Check if the file exists and delete it if it does
    if os.path.exists(xlsx_filename):
        os.remove(xlsx_filename)
    # Scrape URLs and click "next" button four times
    for _ in range(400):
        # Get the page source from Selenium
        page_source = driver.page_source

        # Create BeautifulSoup object
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all the anchor tags containing the page links
        links = driver.find_elements(By.XPATH, '//*[@class="rush-component"]/a[@href]')

        link_urls = [link.get_attribute("href") for link in links]

        # Check if the file is empty
        csv_filename = 'SKU_files/sku.xlsx'
        directory = os.path.dirname(csv_filename)

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        if not os.path.isfile(csv_filename) or os.path.getsize(csv_filename) == 0:
            # If the file is empty, write the header
            ws.append(["Asins"]) 

        # Iterate through each URL
        for url in link_urls:
            # Extract SKU from the URL
            sku = extract_sku_from_url(url)
            # Write SKU to the Excel file
            ws.append([sku])

        # Save the workbook to the Excel file
        wb.save(csv_filename)

        # Click the "next" button
        # Scroll to the specified element
        try:
            # Find the "Next" button element
            next_button = driver.find_element(By.XPATH, './/*[contains(text(), "Next")]')

            # Check if the button is disabled
            
            is_disabled = next_button.get_attribute("aria-disabled")

            if is_disabled == "true":
                break  # Break the loop if the button is disabled

            # Scroll to the "Next" button
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)

            # Click the "Next" button
            next_button.click()
        except (NoSuchElementException, ElementClickInterceptedException):
            # Break the loop if the "Next" button is not found or cannot be clicked
            break

        # Wait for the page to load
        time.sleep(4)
    driver.quit()
    return csv_filename
    # Quit the Selenium WebDriver
    



