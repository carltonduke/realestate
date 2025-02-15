import pandas as pd
from os import environ
import requests
from bs4 import BeautifulSoup


__all__ = ['get_permits', 'get_data_from_keys', 'get_prop_info', 'get_owner_info']


def get_permits(address):
    """Return table of permits pulled from web api.

    Args:
        address (str): Address to search.

    Returns:
        pandas.DataFrame: Resulting table. Has columns
        ['permittype','permit_type_desc','permit_number', 
        'permit_class', 'permit_location','description','tcad_id', 'total_job_valuation']].
    """
    address = address.upper()
    URL_BASE = environ.get("ADDRESS_URL")
    url = URL_BASE + address

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

    try:
        df = pd.DataFrame(data)
    except:
        print("DataFrame creation failed.")
        return None

    if df.empty:
        print(f"No data found for {address}")
        return None

    df = df[['permittype','permit_type_desc','permit_number', 
             'permit_class', 'permit_location','description',
             'tcad_id', 'total_job_valuation']]

    return df


def get_data_from_keys(keys: list, soup: BeautifulSoup) -> dict:
    """Parse html str with regex to find keys.

    Args:
        keys (list): List of strings to parse for.
        soup (BeautifulSoup): Html string.

    Returns:
        dict: k,v pairs from keys and their respective html values.
    """
    result = {}
    for k in keys:
        result[k] = soup.find(string=k+":")
        if result[k]:
            result[k] = result[k].find_next().text.strip()

    return result


def get_prop_info(page_source: str) -> dict:
    """Parse html source for property info.

    Args:
        page_source (str): Raw html string.

    Returns:
        dict: k,v pairs from property info keys and their respective html values.
    """
    soup = BeautifulSoup(page_source, "html.parser")
    property_info = ["Property ID", "Geographic ID", "Tax Office ID"
                    "Type", "Legal Description", "Property Use", "Agent"]
    return get_data_from_keys(property_info, soup)


def get_owner_info(page_source: str) -> dict:
    """Parse html source for owner info.

    Args:
        page_source (str): Raw html string.

    Returns:
        dict: k,v pairs from owner info keys and their respective html values.
    """
    soup = BeautifulSoup(page_source, "html.parser")
    owner_info = ["Name", "Mailing Address", "Owner ID", 
                  "Ownership %", "State Code"]
    return get_data_from_keys(owner_info, soup)
