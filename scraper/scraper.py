from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from os import environ, makedirs
from os.path import dirname, abspath, join, isfile, isdir
from shortuuid import uuid

__all__ = ['get_page', 'write_page']


def get_page(URL: str, address: str) -> str:
    """Get webpage page via headless browser and parse for data.

    Args:
        URL (str): Full URL.
        address (str): Address string used for parsing.

    Returns:
        str: Page HTML from driver's page_source attr.
    """
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(URL)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                    (By.XPATH, 
                    "//*[contains(text(), '{}')]".format(address.upper())))
        )

        source = driver.page_source
    except Exception as e:
        pass
    finally:
        driver.quit()

    return source


def write_page(page_source: str):
    """Write page source to HTML file.

    Args:
        page_source (str): Raw page source HTML.
    """
    outdir = join(dirname(abspath(__file__)), "out")
    if not isdir(outdir):
        os.makedirs(outdir)

    outfile = join(outdir, f"{uuid()}.html")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(page_source)
        print(f"Page written to {outfile}")
    
    

