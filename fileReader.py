import os
import fnmatch
import glob
import time
import threading

from dbHandler import retrieve_doc_names, insert_into_db
from pptConverter import ppt_to_pdf
from textConverter import json_list_creator

dir = r"" + os.getcwd() + "/test files"

def check_new_files():
    current_files = os.listdir(os.getcwd() + "/test files")
    old_files = retrieve_doc_names()
    new_files = (file for file in current_files if file not in old_files)
    return new_files

def sync_files_folder():
    while True:
        for filename in check_new_files():
            if fnmatch.fnmatch(filename, '*.ppt'):
                ppt_to_pdf(glob.glob(os.path.join(dir, filename)))

        for filename in check_new_files():
            if fnmatch.fnmatch(filename, '*.pdf'):
                json_list = json_list_creator(filename)
                insert_into_db(json_list)
                print(filename)
        time.sleep(5)

class sync_files_folder_thread (threading.Thread):
    def run(self):
        print("Synchronizing started")
        sync_files_folder()
        print("Synchronizing finished")

thread1 = sync_files_folder_thread()
thread1.start()
