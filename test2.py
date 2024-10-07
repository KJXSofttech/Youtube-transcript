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
url = "https://www.naukri.com/Dancer-jobs-in-bangalore?experience=3"
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
        # Extract basic details from the job card
        job_title = job.find_element(By.CSS_SELECTOR, 'a.title').text
        company_name = job.find_element(By.CSS_SELECTOR, 'a.comp-name').text
        rating_element = job.find_elements(By.CSS_SELECTOR, 'a.rating')
        ratings = rating_element[0].text if rating_element else "No rating"
        experience = job.find_element(By.CSS_SELECTOR, 'span.expwdth').text
        salary = job.find_element(By.CSS_SELECTOR, 'span.sal').text
        location = job.find_element(By.CSS_SELECTOR, 'span.locWdth').text
        job_description_summary = job.find_element(By.CSS_SELECTOR, 'span.job-desc').text
        skills_elements = job.find_elements(By.CSS_SELECTOR, 'ul.tags-gt li')
        skills = [skill.text for skill in skills_elements]
        posting_date = job.find_element(By.CSS_SELECTOR, 'span.job-post-day').text

        # Click on the job card to open the detailed view
        job_link = job.find_element(By.CSS_SELECTOR, 'a.title').get_attribute('href')
        driver.execute_script("window.open(arguments[0], '_blank');", job_link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)  # Wait for the detailed job page to load

        # Extract detailed job description and other sections
        try:
            job_desc_section = driver.find_element(By.CSS_SELECTOR, 'div.styles_JDC__dang-inner-html__h0K4t').text
        except:
            job_desc_section = "Not available"

        try:
            key_responsibilities_section = driver.find_element(By.XPATH, "//h2[contains(text(), 'Key Responsibilities')]/following-sibling::ul").text
        except:
            key_responsibilities_section = "Not available"

        # Extract role and industry type
        try:
            role = driver.find_element(By.XPATH, "//label[contains(text(), 'Role')]/following-sibling::span/a").text
        except:
            role = "N/A"

        try:
            industry_type = driver.find_element(By.XPATH, "//label[contains(text(), 'Industry Type')]/following-sibling::span/a").text
        except:
            industry_type = "N/A"

        try:
            department = driver.find_element(By.XPATH, "//label[contains(text(), 'Department')]/following-sibling::span/a").text
        except:
            department = "N/A"

        try:
            employment_type = driver.find_element(By.XPATH, "//label[contains(text(), 'Employment Type')]/following-sibling::span").text
        except:
            employment_type = "N/A"

        try:
            role_category = driver.find_element(By.XPATH, "//label[contains(text(), 'Role Category')]/following-sibling::span").text
        except:
            role_category = "N/A"

        # Extract education details
        try:
            education_ug = driver.find_element(By.XPATH, "//label[contains(text(), 'UG')]/following-sibling::span").text
        except:
            education_ug = "N/A"

        try:
            education_pg = driver.find_element(By.XPATH, "//label[contains(text(), 'PG')]/following-sibling::span").text
        except:
            education_pg = "N/A"

        # Extract key skills
        try:
            key_skills_elements = driver.find_elements(By.CSS_SELECTOR, 'div.styles_key-skill_GIPn_ a')
            key_skills = [skill.text for skill in key_skills_elements]
        except:
            key_skills = []

        # Create job dictionary with complete details
        job_data = {
            "Job Title": job_title,
            "Company Name": company_name,
            "Ratings": ratings,
            "Experience": experience,
            "Salary": salary,
            "Location": location,
            "Job Description (Summary)": job_description_summary,
            "Skills": skills,
            "Posting Date": posting_date,
            "Job Description (Detailed)": job_desc_section,
            "Key Responsibilities": key_responsibilities_section,
            "Role": role,
            "Industry Type": industry_type,
            "Department": department,
            "Employment Type": employment_type,
            "Role Category": role_category,
            "Education (UG)": education_ug,
            "Education (PG)": education_pg,
            "Key Skills": key_skills
        }

        # Add the job data to the list
        job_data_list.append(job_data)

        # Close the detailed job tab and switch back to the listing tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)  # Wait before continuing

    except Exception as e:
        print(f"Error extracting data for a job: {e}")

# Print the extracted job data in JSON format
print(json.dumps(job_data_list, indent=4))

# Close the browser
driver.quit()
