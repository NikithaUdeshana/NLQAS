import re
from nltk.tokenize import word_tokenize
from NLQProcessor import sorted_sent_list, query_sentence
from textProcessor import pos_tagging, chunking


# words = pos_tagging(query_sentence)

# def question_type_recognizer(query_sentence):
#     if(words[0][1] == 'WP'):
#         print('Wh question type')
# def pattern_generator(question_type):
#     if(question_type == 'What'):

pattern1 = r"""Chunk: {<WP|WDT|WP$|WRB>?}"""
pattern2 = r"""Chunk: {<VB|VBD|VBG|VBN|VBP|VBZ>?}"""
pattern3 = r"""Chunk: {<DT|JJ|JJR|JJS|NN|NNS|NNP|NNPS>*}"""
pattern4 = r"""Chunk: {<IN|DT|JJ|JJR|JJS|NN|NNS|NNP|NNPS>*}"""


def question_segmenting(query_sentence, pattern):
    tags = pos_tagging(query_sentence)
    chunks = chunking(tags, pattern)
    for chunk in chunks:
        if not (isinstance(chunk, tuple)):
            pattern = r'\w+:?(?=\/)'
            phrase = re.findall(pattern, str(chunk))
            phrase = " ".join(s for s in phrase)
            return phrase

question_word = question_segmenting(query_sentence, pattern1)
verb = question_segmenting(query_sentence, pattern2)
target = question_segmenting(query_sentence, pattern4)
compliment = question_segmenting(query_sentence, pattern4)

answer_pattern = target + " " + verb
# regexPattern = 'r\'(' + answer_pattern.replace(" ","\s") + ')...+\''
regexPattern = answer_pattern.replace(" ","\s")
print(question_word)
print(verb)
print(target)
print(regexPattern)
# print(compliment)
sent_list = list()
for sent in sorted_sent_list:
    match = re.search(r'('+regexPattern+')...+', sent[0])
    if match:
        print(match.group())
        sent_list.append(sent)
for sent in sent_list:
    print(sent)
# for i in sorted_sent_list:
#     print(i)
