import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def cleanHtml(sentence):
    """
        Removes HTML tags from a sentence.

        Args:
            sentence (str): The input sentence.

        Returns:
            str: The sentence without HTML tags.
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    return cleantext

def cleanPunc(sentence):
    """
        Cleans a sentence by removing punctuation and special characters.

        Args:
            sentence (str): The input sentence.

        Returns:
            str: The cleaned sentence.
    """
    cleaned = re.sub(r'[?|!|\'|"|#]', r'', sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]', r' ', cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n", " ")
    return cleaned

def keepAlpha(sentence):
    """
        Keeps only alphabetic characters in a sentence.

        Args:
            sentence (str): The input sentence.

        Returns:
            str: The sentence with only alphabetic characters.
    """
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

def removeStopWords(sentence):
    """
        Removes stopwords from a sentence.

        Args:
            sentence (str): The input sentence.
            stopwords (set): A set of stopwords to be removed.

        Returns:
            str: The sentence without stopwords.
    """
    stop_words = set(stopwords.words('english'))
    stop_words.update(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'may', 'also', 'across', 'among', 'beside', 'however', 'yet', 'within'])
    re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + r")\W", re.I)
    return re_stop_words.sub(" ", sentence)


def stemming(sentence):
    """
        Stems words in a sentence using the Snowball stemmer.

        Args:
            sentence (str): The input sentence.

        Returns:
            str: The sentence with stemmed words.
    """
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

# Define stopwords
stop_words = set(stopwords.words('english'))
stop_words.update(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'may', 'also', 'across', 'among', 'beside', 'however', 'yet', 'within'])

# Define stemmer
stemmer = SnowballStemmer("english")


def preprocess_data(data, clean:bool = 1, punc:bool = 1, alpha:bool = 1, stopword:bool = 1, stemmer:bool = 1):
    """
        Removes HTML tags from a sentence.
    
        Args:
            sentence (str): The input sentence.

        Returns:
            str: The sentence without HTML tags.
    """

    # apply functions
    data = data.str.lower()
    if clean == 1:
        data = data.apply(cleanHtml)
    if punc == 1:
        data = data.apply(cleanPunc)
    if alpha == 1:
        data = data.apply(keepAlpha)
    if stopword == 1:
        data = data.apply(removeStopWords)
    if stemmer == 1:
        data = data.apply(stemming)
    return data

