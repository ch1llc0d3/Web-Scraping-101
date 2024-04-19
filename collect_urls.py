from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# URL of the webpage to scrape
base_url = "https://www.ecohubmap.com/list/business/agriculture/USA"
num_pages = 82  # Total number of pages to scrape

try:
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # Run Chrome in headless mode

    # Start Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    # List to store company URLs
    company_urls = []

    # Iterate through each page
    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}"

        # Send a GET request to the URL
        driver.get(url)

        # Scroll to the bottom of the page to load all content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract the URLs
        elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/company/business/")]')
        page_company_urls = [element.get_attribute('href') for element in elements]

        # Append the URLs to the list
        company_urls.extend(page_company_urls)

        print(f"Scraped page {page} out of {num_pages}")

    # Save the URLs to a Python file named urls.py
    with open('urls.py', 'w') as file:
        file.write("company_urls = [\n")
        for url in company_urls:
            file.write(f'    "{url}",\n')
        file.write("]\n")

    print("Company URLs have been successfully scraped and saved.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close the WebDriver
    driver.quit()
