import string
import operator
import codecs
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def stop_words_elimination(text):

    translate_table = dict((ord(char), None) for char in string.punctuation)
    transformed_text = text.translate(translate_table)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(transformed_text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence

def stemming(text):

    poterStemmer = PorterStemmer()
    stemmed_list = list()
    for w in text:
        stemmed_list.append(poterStemmer.stem(w))
    return stemmed_list

def text_reading(doc):

    file = codecs.open(doc, 'r', 'utf-8')
    text_stream = file.read()
    return text_stream

def text_processing(text_list):
    formatted_text_list = list()

    for text in text_list:
        filtered_text = stop_words_elimination(text)
        stemmed_text = stemming(filtered_text)
        formatted_wordbag = " ".join(str(x) for x in stemmed_text)
        formatted_text_list.append(formatted_wordbag)
    return formatted_text_list

def query_processing(query):

    filtered_text = stop_words_elimination(query)
    stemmed_text = stemming(filtered_text)
    formatted_wordbag = " ".join(str(x) for x in stemmed_text)
    return formatted_wordbag

def vectorizing(doc_list):

    tfidf_vectorizer = TfidfVectorizer()
    tfidftest_matrix = tfidf_vectorizer.fit_transform(doc_list)
    return tfidftest_matrix

def ranking_documents(document_vector, item_list):
    similarity = (cosine_similarity(document_vector[0:1], document_vector))
    ranked_docs = (zip(item_list, similarity[0, 1:]))
    ranked_docs = (x for x in ranked_docs if(x[1]>0))
    sorted_docs = sorted((doc for doc in ranked_docs), key=operator.itemgetter(1))
    sorted_docs.reverse()
    return sorted_docs


def pos_tagging(sample_sentence):
    try:
        words = nltk.word_tokenize(sample_sentence)
        tagged = nltk.pos_tag(words)
        return tagged
    except Exception as e:
        print(str(e))

def chunking(tagged, chunkGram):
    chunkParser = nltk.RegexpParser(chunkGram)
    chunked = chunkParser.parse(tagged)
    return chunked