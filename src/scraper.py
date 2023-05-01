import pandas as pd
import requests
from bs4 import BeautifulSoup

import requests
from urllib.parse import urlparse

def is_scraping_allowed(url):
    """
    Checks if scraping is allowed for the given URL.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if scraping is allowed, False otherwise.
    """
    # Parse the URL to extract the domain.
    domain = urlparse(url).netloc

    # Get the URL for the robots.txt file for the domain.
    robots_url = f"https://{domain}/robots.txt"

    # Send a GET request to the robots.txt file.
    try:
        response = requests.get(robots_url)
    except:
        # If there was an error, assume scraping is not allowed.
        return False

    # Check if the status code of the response is OK.
    if response.status_code != 200:
        # If not, assume scraping is not allowed.
        return False

    # Parse the robots.txt file.
    robots_txt = response.text

    # Check if the user-agent "*" is disallowed from scraping any pages.
    #if "User-agent: *\nDisallow: /" in robots_txt:
    #    return False

    # Check if the user-agent "*" is specifically disallowed from scraping the given URL.
    if f"User-agent: *\nDisallow: {url}" in robots_txt:
        return False

    # If none of the above conditions are met, assume scraping is allowed.
    return True


def scrape_website(url):
    """
    Scrapes the text of a website's landing page if allowed by its robots.txt file,
    and removes unimportant HTML elements like the menu and footer.
    """
    try:
        # Send a request to the website's robots.txt file to check if scraping is allowed
        robots_url = url.rstrip('/') + '/robots.txt'
        robots = requests.get(robots_url).text

        # If scraping is allowed, send a request to the website's landing page
        if 'User-agent: *\nDisallow:' in robots:
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')

            # Remove unimportant HTML elements like the menu and footer
            for tag in soup(['nav', 'header', 'footer']):
                tag.decompose()

            # Extract the visible text from the HTML
            text = soup.get_text(separator=' ')

            # Return the extracted text
            return text
        else:
            # If scraping is not allowed, return a special message
            return 'Scraping not allowed'
    except:
        # If an error occurs, return a special message
        return 'Error scraping'


# Read the CSV file into a pandas dataframe
df = pd.read_csv('../data/raw/startup_list_seminar.csv')

# Create a new dataframe to store the scraped data
new_df = pd.DataFrame(columns=['website_url', 'text'])

# Loop over each URL in the dataframe
for i, url in enumerate(df['website_url']):
    if i >= 10:
        break
    # Scrape the website and add the URL and text to the new dataframe
    allowed = is_scraping_allowed(url)
    print(allowed)
    if allowed:
        text = scrape_website(url)
    else:
        text = None

    # print(text)
    new_df = pd.concat([new_df, pd.DataFrame([[url, allowed, text]], columns=['url', 'allowed', 'text'])], ignore_index=True)

# Save the new dataframe to a CSV file
print("test")
new_df.to_csv('startup_list_seminar-v0_1.csv', index=False)
