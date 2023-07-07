import sys
sys.path.insert(0,"src")
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from nltk.corpus import stopwords
from DataPreprocessing.Preprocessing_en import *



class TestPreprocessing(unittest.TestCase):
        
    def test_cleanHtml(self):
        # Test case 1: HTML tags are present in the sentence
        sentence1 = "<p>This is a <b>sample</b> sentence.</p>"
        expected1 = " This is a  sample  sentence. "
        self.assertEqual(cleanHtml(sentence1), expected1)

        # Test case 2: HTML tags are not present in the sentence
        sentence2 = "This is a sample sentence."
        expected2 = "This is a sample sentence."
        self.assertEqual(cleanHtml(sentence2), expected2)

        # Test case 3: Empty sentence
        sentence3 = ""
        expected3 = ""
        self.assertEqual(cleanHtml(sentence3), expected3)

    def test_cleanPunc(self):
        # Test case 1: Sentence with punctuation and special characters
        sentence1 = "This is a sample sentence! It includes punctuation, quotes, and other special characters."
        expected1 = "This is a sample sentence It includes punctuation  quotes  and other special characters"
        self.assertEqual(cleanPunc(sentence1), expected1)

        # Test case 2: Sentence without punctuation and special characters
        sentence2 = "This is a sample sentence without any punctuation or special characters"
        expected2 = "This is a sample sentence without any punctuation or special characters"
        self.assertEqual(cleanPunc(sentence2), expected2)

        # Test case 3: Empty sentence
        sentence3 = ""
        expected3 = ""
        self.assertEqual(cleanPunc(sentence3), expected3)

    def test_keepAlpha(self):
        # Test case 1: Sentence with alphanumeric and non-alphabetic characters
        sentence1 = "This is a sample sentence! It includes123 numbers and special characters."
        expected1 = "This is a sample sentence  It includes  numbers and special characters"
        self.assertEqual(keepAlpha(sentence1), expected1)

        # Test case 2: Sentence with only alphabetic characters
        sentence2 = "This is a sample sentence with only alphabetic characters"
        expected2 = "This is a sample sentence with only alphabetic characters"
        self.assertEqual(keepAlpha(sentence2), expected2)

        # Test case 3: Empty sentence
        sentence3 = ""
        expected3 = ""
        self.assertEqual(keepAlpha(sentence3), expected3)

    def test_removeStopWords(self):
        # Test case 1: Sentence with stopwords
        sentence1 = "This is a sample sentence with some stopwords such as the, and, of"
        expected1 = '   sample sentence   stopwords       of'
        self.assertEqual(removeStopWords(sentence1), expected1)

        # Test case 2: Sentence without stopwords
        sentence2 = "This is a sample sentence without any stopwords"
        expected2 = '   sample sentence without  stopwords'
        self.assertEqual(removeStopWords(sentence2), expected2)

        # Test case 3: Empty sentence
        sentence3 = ""
        expected3 = ""
        self.assertEqual(removeStopWords(sentence3), expected3)

    def test_stemming(self):
        # Test case 1: Sentence with words to be stemmed
        sentence1 = "Running plays and played games"
        expected1 = "run play and play game"
        self.assertEqual(stemming(sentence1), expected1)

        # Test case 2: Sentence with already stemmed words
        sentence2 = "Running played and games"
        expected2 = "run play and game"
        self.assertEqual(stemming(sentence2), expected2)

        # Test case 3: Empty sentence
        sentence3 = ""
        expected3 = ""
        self.assertEqual(stemming(sentence3), expected3)


    def test_preprocess_data(self):
        data = pd.DataFrame({"text": ["<html>Some text with HTML tags.</html>"]})
        preprocessed_data = preprocess_data(data["text"], clean=True, punc=True, alpha=True, stopword=True, stemmer=True)
        expected_output = ["text html tag"]
        self.assertEqual(preprocessed_data.values.tolist(), expected_output)

        data = pd.DataFrame({"text": ["<html>Some text with HTML tags.</html>"]})
        preprocessed_data = preprocess_data(data["text"], clean=False, punc=False, alpha=False, stopword=False, stemmer=False)
        expected_output = ["<html>some text with html tags.</html>"]
        self.assertEqual(preprocessed_data.values.tolist(), expected_output)

if __name__ == '__main__':
    unittest.main()
