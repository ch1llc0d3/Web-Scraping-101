# extract_data.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from urls import company_urls  # Import the company URLs from urls.py

try:
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # Run Chrome in headless mode

    # Start Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    # Create and open a CSV file to save the data
    with open('company_emails.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Iterate through each company URL and extract data
        for url in company_urls:
            # Send a GET request to the URL
            driver.get(url)

            # Extract company name and email address
            company_name = driver.find_element(By.CLASS_NAME, 'CompaniesContainer_spotName__0MyfK').text
            email = driver.find_element(By.CLASS_NAME, 'CompaniesContainer_infoUrl__Sd6Lg').get_attribute('href').replace('mailto:', '')

            # Write data to CSV file
            writer.writerow({'Company Name': company_name, 'Email': email})

    print("Data has been successfully scraped and saved.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close the WebDriver
    driver.quit()
