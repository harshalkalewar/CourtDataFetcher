from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



class Scraper:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)

    def get_case_details(self, case_type_input, case_number_input, year_input):

        
        self.driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.ID, "captcha-code"))
        )

        captcha_code = self.driver.find_element(By.ID, "captcha-code").text


        case_type = self.driver.find_element(By.NAME, "case_type")
        case_number = self.driver.find_element(By.NAME, "case_number")
        year = self.driver.find_element(By.NAME, "case_year")
        captcha_input = self.driver.find_element(By.ID, "captchaInput")

        # Selecting Case Type
        select_object1 = Select(case_type)
        select_object1.select_by_value(case_type_input)

        # Sending case number
        case_number.send_keys(case_number_input)
        captcha_input.send_keys(captcha_code)

        #Selecting Case Year
        select_object2 = Select(year)
        select_object2.select_by_value(year_input)


        submit_button = self.driver.find_element(By.ID, "search")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        self.driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(2)


        WebDriverWait(self.driver, 6).until(
                    ec.presence_of_element_located((By.XPATH, f"//table[contains(., '{case_type_input}') and contains(., '{case_number_input}')]"))
                )


        #EXTRACT DATA

        table_html = self.driver.find_element(By.XPATH, "//table").get_attribute("outerHTML")
        soup = BeautifulSoup(table_html, "html.parser")
        row = soup.find("tbody").find("tr")
        cols = row.find_all("td")


        case_no_status_html = cols[1]
        case_no_text = case_no_status_html.get_text(separator=" ", strip=True).split("[")[0].strip()
        status = case_no_status_html.find("font").text.strip()
        orders_link = case_no_status_html.find("a", href=True)["href"]

        petitioner_respondent = cols[2].get_text(separator=" ", strip=True)
        petitioner, _, respondent = petitioner_respondent.partition("VS.")

        next_date = last_date = court_no = "NA"
        if len(cols) >= 4:
            date_info = cols[3].decode_contents().strip().split("<br/>")

            # Extract based on known labels
            for item in date_info:
                clean = BeautifulSoup(item, "html.parser").get_text(strip=True)
                if clean.startswith("NEXT DATE:"):
                    next_date = clean.replace("NEXT DATE:", "").strip() or "NA"
                elif clean.startswith("Last Date:"):
                    last_date = clean.replace("Last Date:", "").strip() or "NA"
                elif clean.startswith("COURT NO:"):
                    court_no = clean.replace("COURT NO:", "").strip() or "NA"



        # EXTRACTING LASTEST ORDER LINK
        self.driver.get(orders_link)

        time.sleep(5)

        table = self.driver.find_element(By.ID, "caseTable")
        rows = table.find_element(By.TAG_NAME, "tbody")

        cols = rows.find_elements(By.TAG_NAME, "tr")
        link = None

        for col in cols:
            link = col.find_element(By.TAG_NAME, "a").get_attribute("href")
            break


        result = {
            "case_number": case_no_text,
            "status": status,
            "orders_link": orders_link,
            "petitioner": petitioner.strip(),
            "respondent": respondent.strip(),
            "next_date": next_date,
            "last_date": last_date,
            "court_number": court_no,
            "latest_order_link" : link
        }


        self.driver.quit()
        
        return result

        

