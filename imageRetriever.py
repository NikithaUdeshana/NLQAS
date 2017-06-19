from dbHandler import retrieve_image_list
from patternRecognizer import pattern_recognizer
from textProcessor import text_processing, query_processing, vectorizing, ranking_documents
import base64
import os



def image_retrieval(query_sentence):
    images = {}
    suggested_images = {}
    image_text_list = list()
    image_list = retrieve_image_list()
    for image in image_list:
        images[image['image_path']] = [image['text']]
        image_text_list.append(image['text'])

    for answer in pattern_recognizer(query_sentence):
        formatted_answer = query_processing(answer)
        formatted_text_list = text_processing(image_text_list)
        formatted_text_list.insert(0, formatted_answer)
        word_matrix = vectorizing(formatted_text_list)
        sorted_image_list = ranking_documents(word_matrix, images.keys())
        img = list()
        for image in sorted_image_list:
            img.append(image[0])
        answer_new = str(answer).replace("\n","<br>")
        dict = {answer_new: img}
        suggested_images.update(dict)
    return suggested_images

# for i in image_retrieval("Who are database users?").items():
#     print(i)
