import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from tenacity import retry, wait_fixed, stop_after_attempt

# Setup logging
logging.basicConfig(level=logging.INFO)

@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/134.0.0.0 Safari/537.36',
        'Referer': 'https://www.census.gov/quickfacts/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    params = {
        'type': 'geo',
        'search': 'new',
    }

    response = requests.get(url, params=params, headers=headers)
    if not response.ok:
        logging.warning(f"Failed to fetch {url}: {response.status_code}")
        response.raise_for_status()
    return response.text

def parse_quickfacts_table(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table')
    if not table:
        logging.error("No table found on the page.")
        return None
    df = pd.read_html(str(table))[0]
    return df

def clean_data(df):
    df.columns = ['Data Item', 'Puerto Rico', 'United States']
    df = df.dropna()
    df['Data Item'] = df['Data Item'].str.strip()
    return df

def main():
    url = 'https://www.census.gov/quickfacts/table/PST045215/78030,00'
    html = fetch_page(url)
    df = parse_quickfacts_table(html)
    if df is not None:
        cleaned_df = clean_data(df)
        cleaned_df.to_csv("quickfacts_data.csv", index=False)
        logging.info("Data saved to quickfacts_data.csv")

if __name__ == "__main__":
    main()
