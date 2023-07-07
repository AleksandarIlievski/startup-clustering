import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urlparse
import pandas as pd
import os
import json

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

def remove_cookie_banners(soup):
    """
        Removes elements related to cookie consent banners from the given BeautifulSoup object.

        Args:
            soup (BeautifulSoup): BeautifulSoup object containing the webpage content.

        Note:
            The function may not remove all types of cookie banners as it relies on specific
            classes and IDs. Adjust classes_to_remove and patterns as needed.
        """
    # Find and remove elements with classes containing classes_to_remove content
    classes_to_remove = ['cookie', 'banner', 'popup', 'modal', "cc-dialog", "gdpr-content", "ccform"]  # Customize as needed
    for class_name in classes_to_remove:
        elements = soup.select(f'[class*={class_name}]')
        for element in elements:
            element.extract()

    # Find and remove elements with IDs containing cookie-law-info-bar
    elements = soup.select('[id*=cookie-law-info-bar]')
    for element in elements:
        element.extract()

    # Find and remove elements with classes or IDs containing classes_to_remove content
    pattern = re.compile(r'class=["\'].*?\bcookie\b.*?["\']|id=["\'].*?\bcookie\b.*?["\']')
    tags_with_cookie = soup.find_all(attrs={"class": pattern, "id": pattern})
    for tag in tags_with_cookie:
        tag.extract()
    # Find and remove elements with classes or IDs containing classes_to_remove content
    pattern = re.compile(r'class=["\'].*?\bcc\b.*?["\']|id=["\'].*?\bcc\b.*?["\']')
    tags_with_cookie = soup.find_all(attrs={"class": pattern, "id": pattern})
    for tag in tags_with_cookie:
        tag.extract()

def getWebsiteText(url):
    """
        Retrieves the text content of the webpage at the given URL.

        Args:
            url (str): The URL of the webpage to scrape.

        Returns:
            str: The text content of the webpage.
                 If an error occurs during the request or if the status code is not 200,
                 an error message is returned instead.
        """
    # Headers with Accept-Language set to English
    headers = {
        'Accept-Language': 'en-US,en;q=0.1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send a request to the website and get the response
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            #print(f"The link {url} is working.")
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a'):
                a_tag.extract()
            text = soup.getText()
            return text
        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        # Handle the error here
        if 'response' not in locals():
            return "Error: Failed to get response"
        return f"Error: {response.status_code}"
    
def getWebsiteText_v2(url):
    """
        Retrieves the text content of the webpage at the given URL and removes cookie banners.

        Args:
            url (str): The URL of the webpage to scrape.

        Returns:
            str: The text content of the webpage, with cookie banners removed.
                 If an error occurs during the request or if the status code is not 200,
                 an error message is returned instead.
        """
    # Headers with Accept-Language set to English and Cookie consent
    headers = {
        'Accept-Language': 'en-US,en;q=0.1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Cookie': 'consent=true'  # Add the cookie consent header
    }

    # Send a request to the website and get the response
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # remove all <a> (button with href link)
            for a_tag in soup.find_all('a'):
                a_tag.extract()
            remove_cookie_banners(soup)  # Remove elements with classes or IDs containing specified content
            text = soup.get_text()
            return text
        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        # Handle the error here
        if 'response' not in locals():
            return "Error: Failed to get response"
        return f"Error: {response.status_code}"
    
def format_string(input_string):
    """
        Formats the input string by replacing multiple whitespaces with a single space.

        Args:
            input_string (str): The string to format.

        Returns:
            str: The formatted string.
        """

    # Replace all other Unicode letters with an empty string
    #formatted_string = ''.join(c if unicodedata.category(c)[0] != 'P' else ' ' for c in formatted_string)

    # Remove markdowns and extra whitespaces
    formatted_string = re.sub(r'\s+', ' ', input_string)

    return formatted_string.strip()

def remove_sentence_with_keyword(text, keyword):
    """
        Removes sentences that contain the specified keyword from the text.

        Args:
            text (str): The text to process.
            keyword (str): The keyword to look for.

        Returns:
            str: The processed text.
        """
    # Split the text into sentences using regex pattern
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Remove sentences that contain the keyword
    filtered_sentences = [sentence for sentence in sentences if keyword.lower() not in sentence.lower()]

    # Join the remaining sentences back into a single string
    modified_text = ' '.join(filtered_sentences)

    return modified_text

def get_text_and_json(input_df):
    """
        Retrieves the text content of webpages based on the provided DataFrame and creates a dictionary of processed data.

        Args:
            input_df (pandas.DataFrame): The DataFrame containing the input data.
                                         It should have columns named 'name', 'original_idx', 'check_robots', and 'website_url'.

        Returns:
            dict: A dictionary where the keys are row indices from the input DataFrame, and the values are dictionaries
                  containing processed data for each row. The dictionaries have the following keys:
                  - 'name': The name from the input DataFrame.
                  - 'original_idx': The original index from the input DataFrame.
                  - 'website_url': The URL from the input DataFrame.
                  - 'website_text': The processed text content of the webpage.
    """
    data = input_df
    data['original_idx'] = data.index
    data = data.loc[data["check_robots"] == True]

    data_dict = {}
    # Iterate over the rows of the DataFrame
    for index, row in data.iterrows():
        print(index)
        name = row['name']
        id = row['original_idx']
        url = row['website_url']

        text = getWebsiteText_v2(url)
        
        # Remove empty lines
        lines = text.splitlines()
        new_lines = [line for line in lines if line]
        new_text = "\n".join(new_lines)
        website_text = format_string(new_text)

        # Create a dictionary for the current row and add it to the data_dict
        row_dict = {
            'name': name,
            'original_idx': id,
            'website_url': url,
            'website_text': website_text
        }
        data_dict[index] = row_dict
    
    return data_dict


