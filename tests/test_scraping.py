import unittest
import pandas as pd
import requests
import re
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.Web_Scraping.basic_functions import (is_scraping_allowed, remove_cookie_banners, getWebsiteText,
                                              getWebsiteText_v2, format_string, remove_sentence_with_keyword,
                                              get_text_and_json)


class TestScraper(unittest.TestCase):

    def test_is_scraping_allowed(self):
        url = "http://example.com"
        with patch('requests.get') as mock_get:
            # Simulate the response
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = "User-agent: *\nDisallow: /test"
            mock_get.return_value = mock_resp

            self.assertTrue(is_scraping_allowed(url))

            # Change the mock to simulate a disallowed URL.
            mock_resp.text = f"User-agent: *\nDisallow: {url}"
            self.assertFalse(is_scraping_allowed(url))

            # Test case where requests.get() raises an exception.
            mock_get.side_effect = Exception()
            self.assertFalse(is_scraping_allowed(url))

            # Test case where status code is not 200.
            mock_resp.status_code = 404
            mock_get.side_effect = None
            mock_get.return_value = mock_resp
            self.assertFalse(is_scraping_allowed(url))

    def test_remove_cookie_banners(self):
        soup = BeautifulSoup('<div class="cookie-banner">Hello, world!</div>', 'html.parser')
        remove_cookie_banners(soup)
        self.assertFalse(soup.find(class_="cookie-banner"))

    def test_getWebsiteText(self):
        url = "http://example.com"
        with patch('requests.get') as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b"<html><body><p>Hello, world!</p></body></html>"
            mock_get.return_value = mock_resp

            self.assertEqual(getWebsiteText(url), "Hello, world!")

            # Test case where requests.get() raises an exception.
            mock_get.side_effect = Exception()
            self.assertEqual(getWebsiteText(url), "Error: Failed to get response")

            # Test case where status code is not 200.
            mock_resp.status_code = 404
            mock_get.side_effect = None
            mock_get.return_value = mock_resp
            self.assertEqual(getWebsiteText(url), "Error: 404")

    def test_getWebsiteText_v2(self):
        url = "http://example.com"
        with patch('requests.get') as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b"<html><body><p>Hello, world!</p></body></html>"
            mock_get.return_value = mock_resp

            self.assertEqual(getWebsiteText_v2(url), "Hello, world!")

            # Test case where requests.get() raises an exception.
            mock_get.side_effect = Exception()
            self.assertEqual(getWebsiteText_v2(url), "Error: Failed to get response")

            # Test case where status code is not 200.
            mock_resp.status_code = 404
            mock_get.side_effect = None
            mock_get.return_value = mock_resp
            self.assertEqual(getWebsiteText_v2(url), "Error: 404")

    def test_format_string(self):
        input_string = "  Hello,  world!  "
        self.assertEqual(format_string(input_string), "Hello, world!")

    def test_remove_sentence_with_keyword(self):
        text = "Hello, world! This is a test."
        keyword = "test"
        self.assertEqual(remove_sentence_with_keyword(text, keyword), "Hello, world!")

        # Test case with no match
        keyword = "no-match"
        self.assertEqual(remove_sentence_with_keyword(text, keyword), text)

    @patch('src.Web_Scraping.basic_functions.getWebsiteText_v2')
    @patch('src.Web_Scraping.basic_functions.format_string')
    def test_get_text_and_json(self, mock_format_string, mock_getWebsiteText_v2):
        # Create a sample DataFrame for testing
        data = pd.DataFrame({
            'name': ['Website 1', 'Website 2'],
            'original_idx': [0, 1],
            'check_robots': [True, False],
            'website_url': ['http://example.com', 'http://example.org']
        })

        # Mock the behavior of getWebsiteText_v2
        mock_getWebsiteText_v2.return_value = 'Sample website text'

        # Mock the behavior of format_string
        mock_format_string.return_value = 'Formatted website text'

        # Call the function being tested
        result = get_text_and_json(data)
        result
        # Assert that the mock functions were called with the correct arguments
        mock_getWebsiteText_v2.assert_called_with('http://example.com')
        mock_format_string.assert_called_with('Sample website text')

        # Assert the expected output
        expected_result = {
            0: {
                'name': 'Website 1',
                'original_idx': 0,
                'website_url': 'http://example.com',
                'website_text': 'Formatted website text'
            }
        }
        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
