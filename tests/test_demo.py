import unittest
from src.demo import say_hello
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from src.scraper import scrape_website


class TestDemo(unittest.TestCase):

    def setUp(self):

        # defining input shared across tests
        self.dummy_name = 'dummy'

    def test_say_hello(self):

        # get output of say_hello
        output = say_hello(name=self.dummy_name)

        # check output
        self.assertEqual(output, 'hello dummy')

    def tearDown(self):

        # define actions that are carried out after each test
        pass

class TestScraper(unittest.TestCase):

    def test_scrape_website_allowed(self):
        # Test that the scrape_website function returns the expected text when scraping is allowed
        url = 'http://books.toscrape.com/'
        expected_text = 'Books to Scrape - Sandbox'

        actual_text = scrape_website(url)
        self.assertEqual(actual_text.strip(), expected_text)

    def test_scrape_website_not_allowed(self):
        # Test that the scrape_website function returns the expected text when scraping is not allowed
        url = 'http://httpbin.org/deny'
        expected_text = 'Scraping not allowed'

        actual_text = scrape_website(url)
        self.assertEqual(actual_text.strip(), expected_text)

    def test_scrape_website_error(self):
        # Test that the scrape_website function returns the expected text when an error occurs
        url = 'http://thiswebsitedoesnotexist.com'
        expected_text = 'Error scraping'

        actual_text = scrape_website(url)
        self.assertEqual(actual_text.strip(), expected_text)

    def test_scrape_website_remove_html_elements(self):
        # Test that the scrape_website function removes unimportant HTML elements from the scraped text
        url = 'http://books.toscrape.com/'
        expected_text = 'Books to Scrape - Sandbox'

        actual_text = scrape_website(url)
        self.assertNotIn('<nav', actual_text)
        self.assertNotIn('<header', actual_text)
        self.assertNotIn('<footer', actual_text)

    def test_scrape_website_adds_to_dataframe(self):
        # Test that the scrape_website function adds the scraped data to the new dataframe correctly
        url = 'http://books.toscrape.com/'
        expected_df = pd.DataFrame({'website_url': [url], 'text': ['Books to Scrape - Sandbox']})

        df = pd.DataFrame({'website_url': [url]})
        new_df = pd.DataFrame(columns=['website_url', 'text'])

        for url in df['website_url']:
            text = scrape_website(url)
            new_df = pd.concat([new_df, pd.DataFrame([[url, text]], columns=new_df.columns)], ignore_index=True)

        assert_frame_equal(new_df, expected_df)

if __name__ == '__main__':
    unittest.main()
