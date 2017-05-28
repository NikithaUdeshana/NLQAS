import string
import operator
import codecs

from dbHandler import retrieve_documents
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




query_sentence = "what is database?"

text_docs = {}
text_content_list = list()
for data in retrieve_documents():
    text_docs[data['doc_name']] = [data['doc_content']]
    text_content_list.append(data['doc_content'])

formatted_query = query_processing(query_sentence)

formatted_doc_list = text_processing(text_content_list)
formatted_doc_list.insert(0, formatted_query)
word_matrix = vectorizing(formatted_doc_list)
sorted_doc_list = ranking_documents(word_matrix, text_docs.keys())

for item in sorted_doc_list:
    print(item)

retrieved_doc_list = list()
for docs in range(2):
    retrieved_doc_list.append(sorted_doc_list[docs][0])

sentences = list()
for file in retrieved_doc_list:
    for text in text_docs[file]:
        for para in text.split('\x0c'):
            sentences.append(para)
            # sentences.extend(sent_tokenize(para))

print(retrieved_doc_list)

formatted_sent_list = text_processing(sentences)
formatted_sent_list.insert(0, formatted_query)
word_matrix = vectorizing(formatted_sent_list)
sorted_sent_list = ranking_documents(word_matrix, sentences)

for sent in sorted_sent_list:
    print(sent)