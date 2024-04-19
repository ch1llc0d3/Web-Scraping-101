from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from urls import company_urls

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')  # Run Chrome in headless mode

try:
    # Start Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    # Create and open a CSV file to save the data
    with open('company_emails.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Iterate through each URL
        for url in company_urls:
            # Send a GET request to the URL
            driver.get(url)

            # Extract company names and email addresses
            companies = driver.find_elements(By.CLASS_NAME, 'CompaniesContainer_spotName__0MyfK')
            emails = driver.find_elements(By.CLASS_NAME, 'CompaniesContainer_infoUrl__Sd6Lg')

            # Iterate through each company and save the data to the CSV file
            for company, email in zip(companies, emails):
                company_name = company.text
                email_address = email.get_attribute('href').replace('mailto:', '')  # Extract the email address from href
                writer.writerow({'Company Name': company_name, 'Email': email_address})

    print("Data has been successfully scraped and saved.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close the WebDriver
    driver.quit()
