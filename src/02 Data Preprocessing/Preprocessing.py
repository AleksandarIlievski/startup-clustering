import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

def cleanHtml(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    cleantext = cleantext.replace("\n"," ")
    cleantext = cleantext.replace("√ú","Ü")
    cleantext = cleantext.replace("√ü","ß")
    cleantext = cleantext.replace("√∂", "ö")
    cleantext = cleantext.replace("√º", "ü")
    cleantext = cleantext.replace("√§", "ä")
    cleantext = cleantext.replace("&", "und")
    cleantext = cleantext.replace("‚Äú", " ")
    cleantext = cleantext.replace("¬†", " ")
    return cleantext

def cleanPunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned

def keepAlpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z äüöÄÜÖß]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

def removeStopWords(sentence, stopwords):
    # define stopwords
    stop_words = set(stopwords.words('german'))
    stop_words.update(['null','eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun','zehn'])
    re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)   
    return re_stop_words.sub(" ", sentence)

def stemming(sentence):
    # define stemmer
    stemmer = SnowballStemmer("german")
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

def preprocess_data(data):
    # apply functions
    data = data.str.lower()
    data = data.apply(cleanHtml)
    data = data.apply(cleanPunc)
    data = data.apply(keepAlpha)
    data = data.apply(removeStopWords, stopwords=stopwords)
    data = data.apply(stemming)
    return data