import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# define functions
def cleanHtml(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    return cleantext

def cleanPunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'', sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ', cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned

def keepAlpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

def removeStopWords(sentence, stopwords):
    re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)   
    return re_stop_words.sub(" ", sentence)

def stemming(sentence):
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

# define stopwords
stop_words = set(stopwords.words('english'))
stop_words.update(['zero','one','two','three','four','five','six','seven','eight','nine','ten','may','also','across','among','beside','however','yet','within'])

# define stemmer
stemmer = SnowballStemmer("english")


def preprocess_data(data, clean:bool = 1, punc:bool = 1, alpha:bool = 1, stopword:bool = 1, stemmer:bool = 1):
    # apply functions
    data = data.str.lower()
    if clean == 1:
        data = data.apply(cleanHtml)
    if punc == 1:
        data = data.apply(cleanPunc)
    if alpha == 1:
        data = data.apply(keepAlpha)
    if stopword == 1:
        data = data.apply(removeStopWords, stopwords=stopwords)
    if stemmer == 1:
        data = data.apply(stemming)
    return data