import os
import fnmatch
import glob
import time
import threading

from dbHandler import retrieve_doc_names, insert_into_documents, insert_into_images
from ppt_to_pdfConverter import ppt_to_pdf
from pdf_to_textConverter import json_doc_creator
from imageExtrator import image_extractor

dir = r"" + os.getcwd() + "/test files"

def check_new_files():
    current_files = os.listdir(os.getcwd() + "/test files")
    old_files = retrieve_doc_names()
    new_files = (file for file in current_files if file not in old_files)
    return new_files

def sync_files_folder():
    while True:
        print("Synchronizing started")
        json_doc_list = list()
        json_image_list = list()

        for filename in check_new_files():
            if fnmatch.fnmatch(filename, '*.pptx'):
                ppt_to_pdf(glob.glob(os.path.join(dir, filename)))

        for filename in check_new_files():
            if fnmatch.fnmatch(filename, '*.pdf'):
                json_doc = json_doc_creator(filename)
                json_image_list = image_extractor(filename)
                json_doc_list.append(json_doc)
                print(filename)
        if json_doc_list:
            insert_into_documents(json_doc_list)
        if json_image_list:
            insert_into_images(json_image_list)
        print("Synchronizing finished")
        time.sleep(60*60*60*6)

class sync_files_folder_thread (threading.Thread):
    def run(self):
        sync_files_folder()

thread1 = sync_files_folder_thread()
thread1.start()