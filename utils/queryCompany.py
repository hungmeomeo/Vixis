from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_target_price(url):
    """Fetch the target price from the consensus page."""

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    td_elements = soup.find_all("td", class_="c-table__cell c-table__cell--dotted c-table__cell--bold")

    if len(td_elements) > 4:
        price_spans = td_elements[4].find_all("span", class_="c-table__content")
        if price_spans:
            return price_spans[0].get_text(strip=True).split()[0]  # Extract price
    return None

def query_company(company_name, recursive_call=True):
    """Search for a company and extract financial data from Boursorama."""
    url = f"https://www.boursorama.com/recherche/?query={company_name}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data. Status Code: {response.status_code}")

    response_url = response.url
    soup = BeautifulSoup(response.text, "html.parser")

    if response_url.startswith("https://www.boursorama.com/cours/"):
        output = {}
        output['Main url'] = response_url
        # Extract table row data for "1 an", "3 ans", "5 ans"
        for row in soup.find_all("tr", class_="c-table__row"):
            first_col = row.find("th")
            if first_col and first_col.get_text(strip=True) in ["1 an", "3 ans", "5 ans"]:
                data = [cell.get_text(strip=True).replace("\u202f", "") for cell in row.find_all(["th", "td"])]
                output[data[0]] = data[1]

        # Extract numerical values
        values = [
            cell.get_text(strip=True).split()[0] 
            for cell in soup.find_all("td", class_="c-table__cell c-table__cell--dotted c-table__cell--inherit-height c-table__cell--align-top / u-text-left u-text-right u-ellipsis")
        ]

        # Extract years
        years = [
            h3.get_text(strip=True)[-4:]
            for h3 in soup.find_all("h3", class_="c-table__title u-text-uppercase u-text-size-xxxs u-text-normal-whitespace")
            if h3.get_text(strip=True)[-4:].isdigit()
        ]

        # Map values to corresponding years
        for index, year in enumerate(years):
            if index < len(values) and (index + 9) < len(values):  # Avoid IndexError
                output[f'Dividende par action {year}'] = values[index]
                output[f'PER {year}'] = values[index + 9]

        consensus_url = response_url.replace("cours/", "cours/consensus/", 1)
        output['Objectif de cours'] = fetch_target_price(consensus_url) or "Price data unavailable"
        output['Consensus url'] = consensus_url
        return output

    if recursive_call:
        link_tag = soup.find("a", class_="c-link c-link--animated / o-ellipsis")
        if link_tag:
            return query_company(link_tag.text.strip(), recursive_call=False)  # Allow only 1 recursive call

    return {}

@app.get("/query")
def get_stock_info(company_name: str):
    """API endpoint to get stock information."""
    return query_company(company_name)
