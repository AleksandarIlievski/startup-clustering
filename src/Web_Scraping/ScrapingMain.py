import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urlparse
import pandas as pd
import os
import json
from src.Web_Scraping.basic_functions import (get_text_and_json, is_scraping_allowed, remove_cookie_banners, getWebsiteText, getWebsiteText_v2, format_string, remove_sentence_with_keyword)

# Read data from a CSV file
data = pd.read_csv("data/raw/")

# Iterate over each row in the data DataFrame
for i in range(len(data)):
    print(i)  # Print progress information
    url = data['website_url'][i]  # Get the website URL from the current row
    result = is_scraping_allowed(url)  # Check if scraping is allowed for the URL
    data.loc[i, "check_robots"] = result  # Store the result in the 'check_robots' column of the DataFrame

# Write the modified data DataFrame back to a CSV file
# data.to_csv("data/raw/startup_list_0_5000_prep.csv")

# Read data again from the CSV file, this time with an index column specified
data = pd.read_csv("data/raw/", index_col=0)

# Perform web scraping and get the desired data
output_dic = get_text_and_json(data)

# Convert the output dictionary to a JSON object
json_object = json.dumps(output_dic, indent=4, ensure_ascii=False)

# Write the JSON object to a file
path = "data/raw/"
with open(path, "w", encoding='utf-8') as outfile:
    outfile.write(json_object)
