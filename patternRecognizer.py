import re
from NLQProcessor import sorted_sent_list

# for i in sorted_sent_list:
#     print(i)
sent_list = list()
for sent in sorted_sent_list:
    match = re.search(r'(database\sis\s)...+',sent[0])
    if match:
        print(match.group())
        sent_list.append(sent)
for sent in sent_list:
    print(sent)

