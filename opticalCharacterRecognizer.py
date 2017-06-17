import os
import cv2
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
# Path of working folder on Disk
# src_path = os.getcwd() + "/images/"
src_path = "C:/Users/Nikitha Udeshana/PycharmProjects/NaturalLanguageQuestionProcessor/images/"
# def data_uri_to_cv2_img(binary_image):
#     # encoded_data = uri.split(',')[1]
#     numpy_array = np.fromstring(binary_image, np.uint8)
#     img = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
#     return img
#
# # data_uri = "data:image/jpeg;base64,/9j/4AAQ..."
# # img = data_uri_to_cv2_img(data_uri)
# # cv2.imshow(img)

def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(src_path + "gray.png", img)
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # Write the image after pre-processing
    cv2.imwrite(src_path + "thres.png", img)
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "gray.png"))
    return result

def ocr(image_path):
    # image = data_uri_to_cv2_img(binary_image)
    outputText = get_string(image_path)
    outputText = outputText.replace("\n"," ")
    return outputText

def ocr_word_count(outputText):
    wordCount = outputText.split(" ")
    count = 0
    for word in wordCount:
        if not(word == ""):
            count += 1
    return count

# ocr_text = ocr(src_path + "Lecture_6_Integration.pdf-p3-27")
# print(ocr_text)
# word_count = ocr_word_count(ocr_text)
# print("word count: " + ocr_word_count())