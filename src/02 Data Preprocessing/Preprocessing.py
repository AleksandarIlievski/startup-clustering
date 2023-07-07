import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

#function to clean HTML Markups from texts
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


#function to clean the word of any punctuation or special characters
def cleanPunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned

#function to replace different non-alpha-numerical values with ' '
def keepAlpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z äüöÄÜÖß]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

#remove German stop words
def removeStopWords(sentence, stopwords):
    # define stopwords
    stop_words = set(stopwords.words('german'))
    stop_words.update(['null','eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun','zehn', 'Impressum', 'Cookies', 'Datenschutzerklärung', 'AGB', 'Mail', 'Blog', 'Kontakt', 'Unternehmen', 'Lösungen'])
    re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)   
    return re_stop_words.sub(" ", sentence)

#stem words
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

#function to apply previously defined preprocessing to texts
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