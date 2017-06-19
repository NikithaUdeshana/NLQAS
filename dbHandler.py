from pymongo import MongoClient

db_client = MongoClient()
db = db_client['text_database']

def insert_into_documents(data_list):
    collection = db['documents']
    collection.insert_many(data_list)

def insert_into_images(images_list):
    collection = db['images']
    collection.insert_many(images_list)

def retrieve_documents():
    collection = db['documents']
    text_document_list = collection.find()
    return text_document_list

def retrieve_doc_names():
    collection = db['documents']
    doc_names = collection.distinct("doc_name")
    return doc_names

def retrieve_image_list():
    collection = db['images']
    image_list = collection.find()
    return image_list