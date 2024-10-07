from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

# Set up Chrome WebDriver
chrome_driver_path = "/usr/local/bin/chromedriver"  # Adjust the path to your chromedriver
service = Service(chrome_driver_path)
options = Options()

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the Naukri job listing page
url = "https://www.naukri.com/python-developer-jobs-in-bangalore?experience=3"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Find all the job listings
jobs = driver.find_elements(By.CSS_SELECTOR, 'div.srp-jobtuple-wrapper')

# List to hold all job data
job_data_list = []

# Iterate over each job listing
for job in jobs:
    try:
        # Extract job details
        job_title = job.find_element(By.CSS_SELECTOR, 'a.title').text
        company_name = job.find_element(By.CSS_SELECTOR, 'a.comp-name').text
        rating_element = job.find_elements(By.CSS_SELECTOR, 'a.rating')
        ratings = rating_element[0].text if rating_element else "No rating"
        experience = job.find_element(By.CSS_SELECTOR, 'span.expwdth').text
        salary = job.find_element(By.CSS_SELECTOR, 'span.sal').text
        location = job.find_element(By.CSS_SELECTOR, 'span.locWdth').text
        job_description = job.find_element(By.CSS_SELECTOR, 'span.job-desc').text
        skills_elements = job.find_elements(By.CSS_SELECTOR, 'ul.tags-gt li')
        skills = [skill.text for skill in skills_elements]
        posting_date = job.find_element(By.CSS_SELECTOR, 'span.job-post-day').text

        # Create job dictionary
        job_data = {
            "Job Title": job_title,
            "Company Name": company_name,
            "Ratings": ratings,
            "Experience": experience,
            "Salary": salary,
            "Location": location,
            "Job Description": job_description,
            "Skills": skills,
            "Posting Date": posting_date
        }

        # Add the job data to the list
        job_data_list.append(job_data)
    
    except Exception as e:
        print(f"Error extracting data for a job: {e}")

# Print the extracted job data in JSON format
print(json.dumps(job_data_list, indent=4))

# Close the browser
driver.quit()
