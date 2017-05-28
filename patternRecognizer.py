import re
from NLQProcessor import sorted_sent_list

sent_list = list()
for sent in sorted_sent_list:
    match = re.search(r'database\sis',sent[0])
    if match:
       sent_list.append(sent)
for sent in sent_list:
    print(sent)

