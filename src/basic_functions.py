from langdetect import detect
import requests
from bs4 import BeautifulSoup

def getWebsiteText(url):
    """
    Retrieves the raw text content of a website if scraping is allowed.

    Args:
        url (str): The URL of the website to retrieve.

    Returns:
        str: The raw text content of the website, or an error message if unsuccessful.
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
            text = soup.getText()
            return text
        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        # Handle the error here
        if 'response' not in locals():
            return "Error: Failed to get response"
        return f"Error: {response.status_code}"

def detectLang(textfile):
    """
    Detects the language of a given text file.

    Args:
        textfile (str): The path to the text file to analyze.

    Returns:
        str: The language code of the text in the file, or an error message if unsuccessful.
    """

    with open(textfile, 'r', encoding="utf-8") as f:
        text = f.read()

        try:
            lang = detect(text)
            return lang
        except Exception as e:
            return f"Error: {str(e)}"

    
def getLength(textfile):
    """
    Gets the length of a given text file.

    Args:
        textfile (str): The path to the text file to analyze.

    Returns:
        int: The length of the text file.
    """

    with open(textfile, 'r', encoding="utf-8") as f:
        text = f.read()
        num_chars = len(text)

    return num_chars



