import os

files = os.listdir(os.getcwd() + "/test files")

for filename in files:
    print(filename)