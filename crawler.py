import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def get_detailed_info(driver, url):
    driver.get(url)
    time.sleep(3)  # Adjust time based on page load times
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_tag = soup.find('a', {"data-fancybox": True})
    image_url = 'https://www.gedenktafeln-in-berlin.de' + image_tag['href'] if image_tag else None
    
    description_div = soup.find('div', class_='boxklammer-content')
    if description_div:
        description_parts = description_div.find_all(text=True)
        description = ' '.join(description_parts).strip().replace('\n', ' ')
    else:
        description = "Description not found"
    
    return {"imageURL": image_url, "description": description}

SKIP_RECORDS = 1394  # Update this based on where you left off

# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument('headless')  # Uncomment for headless mode
driver = webdriver.Chrome(service=service, options=options)

# URL to access
url = "https://www.gedenktafeln-in-berlin.de/gedenktafeln/ajax-search?tx_gedenktafeln_pi1%5Bcontroller%5D=Tafeln&tx_gedenktafeln_pi1%5BcurrentPage%5D=1&tx_gedenktafeln_pi1%5Bmodus%5D=10&tx_gedenktafeln_pi1%5Bortsteil%5D=bz-3&type=9999&cHash=86a85e976e9a51ff1f343a3dff6b4b80"

# Check if the data directory exists, create it if not
data_dir = os.path.join(os.getcwd(), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the path for the data.json file within the data directory
data_file_path = os.path.join(data_dir, 'data.json')

# Open the file in append mode 
with open(data_file_path, 'a', encoding='utf-8') as f:
    # Navigate to the URL and collect links
    driver.get(url)
    time.sleep(10)  # Adjust based on page load times
    
    # Parse the initial page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list_container = soup.find('ul', class_='list-group list-group-flush')
    
    if list_container:
        items = list_container.find_all('li', class_='list-group-item px-0')
        total_items = len(items)
        print(f"Total items to process: {total_items}")
    
        for index, item in enumerate(items[SKIP_RECORDS:], start=1 + SKIP_RECORDS):
            link_tag = item.find('a')
            if link_tag:
                title = link_tag.get('title')
                href = link_tag.get('href')
                full_url = f"https://www.gedenktafeln-in-berlin.de{href}"
                
                print(f"Processing item {index} of {total_items}: {title}")
                # Fetch detailed information for each item
                detailed_info = get_detailed_info(driver, full_url)
                data_to_write = {
                    "url": full_url,
                    "title": title,
                    **detailed_info
                }
                
                # Append the data as a JSON string followed by a newline
                f.write(json.dumps(data_to_write, ensure_ascii=False) + '\n')

# Close the Selenium WebDriver
driver.quit()
