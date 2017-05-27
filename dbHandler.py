from pymongo import MongoClient

def insert_into_db(data_list):
    db_client = MongoClient()
    db = db_client['text_database']
    collection = db['documents']
    collection.insert_many(data_list)

def retrieve_documents():
    db_client = MongoClient()
    db = db_client['text_database']
    collection = db['documents']
    text_document_list = collection.find()
    return text_document_list