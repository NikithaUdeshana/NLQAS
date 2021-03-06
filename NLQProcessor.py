from textProcessor import query_processing, text_processing, vectorizing, ranking_documents
from dbHandler import retrieve_documents


def NLQprocessing(query_sentence):

    text_docs = {}
    text_content_list = list()
    courses_list = {}
    for data in retrieve_documents():
        text_docs[data['doc_name']] = [data['doc_content']]
        courses_list[data['doc_name']] = data['course']
        text_content_list.append(data['doc_content'])

    formatted_query = query_processing(query_sentence)

    formatted_doc_list = text_processing(text_content_list)
    formatted_doc_list.insert(0, formatted_query)
    word_matrix = vectorizing(formatted_doc_list)
    sorted_doc_list = ranking_documents(word_matrix, text_docs.keys())

    # for item in sorted_doc_list:
    #     print(item)

    retrieved_doc_list = list()
    for docs in range(4):
        retrieved_doc_list.append(sorted_doc_list[docs][0])

    sentences = list()
    for file in retrieved_doc_list:
        for text in text_docs[file]:
            for para in text.split('\x0c'):
                sentences.append(para)
                # sentences.extend(sent_tokenize(para))

    # print(retrieved_doc_list)

    formatted_sent_list = text_processing(sentences)
    formatted_sent_list.insert(0, formatted_query)
    word_matrix = vectorizing(formatted_sent_list)
    sorted_sent_list = ranking_documents(word_matrix, sentences)

    # for sent in sorted_sent_list:
    #     print(sent)
    return sorted_sent_list
