from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

__all__ = ['get_page']


def get_page(URL: str) -> str:
    """Get webpage page via headless browser and parse for data.

    Args:
        URL (str): Full URL.
        pid (int): PropertyID value.
        year (str, optional): Year of data collection. Defaults to 2024.

    Returns:
        str: Page HTML filtered to body.
    """
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(URL)
        #WebDriverWait(driver, 60).until(
            #EC.presence_of_element_located((By.XPATH, "//*[@id='root']//div")))
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='address']"))
        )       
        #source, text = driver.page_source, driver.find_element(By.TAG_NAME, "body").text
        #source = driver.page_source
        #text = driver.find_element_by_xpath("//a[text()='address']")
        #content = source if source else text
        #content = text if text else source   
    finally:
        driver.quit()

    return element


if __name__ == "__main__":
    load_dotenv()
    URL = os.environ.get("SCRAPER_URL")

    page = get_page(URL)
    
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(page)

