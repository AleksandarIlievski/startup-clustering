import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the specified URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and remove the footer element(s) from the parsed HTML
    for footer in soup.find_all('footer'):
        footer.extract()

    # Extract all the text from the remaining HTML
    text = soup.get_text()

    # Remove any leading or trailing white spaces and return the text
    return text.strip()

# Create a dataframe with website URLs
df = pd.read_csv("../data/raw/startup_list_seminar.csv")

# Scrape each website URL and store the results in a new column

df['text'] = df['website_url'].apply(scrape_website)
