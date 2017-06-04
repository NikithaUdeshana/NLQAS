import re
import operator

from NLQProcessor import sorted_sent_list, query_sentence
from textProcessor import pos_tagging, chunking, stop_words_elimination, stemming

answer_list = list()
sorted_sent_list = [list(sent) for sent in sorted_sent_list]

def text_normalizing(text):
    words = stop_words_elimination(text)
    stems = stemming(words)
    pattern = " ".join(stem for stem in stems)
    return pattern

def question_segmenting(query_sentence, pattern):
    tags = pos_tagging(query_sentence)
    chunks = chunking(tags, pattern)
    for chunk in chunks:
        if not (isinstance(chunk, tuple)):
            pattern = r'\w+:?(?=\/)'
            phrase = re.findall(pattern, str(chunk))
            phrase = " ".join(s for s in phrase)
            return phrase

def answer_pattern_matching(answer_pattern):
    regexPattern = answer_pattern[0].replace(" ", "\s")
    for sent in sorted_sent_list:
        match = re.search(r'('+regexPattern+')', sent[0], re.IGNORECASE)
        if match:
            # print(match.group())
            sent[1] = sent[1] + 0.2 * answer_pattern[1]
            answer_list.append(sent)

def pattern_lemma_matching(answer_pattern):
    pattern = text_normalizing(answer_pattern[0])
    regexPattern = pattern.replace(" ", "\s")
    for sent in sorted_sent_list:
        sent_words = text_normalizing(sent[0])
        match = re.search(r'(' + regexPattern + ')', sent_words, re.IGNORECASE)
        if match:
            # print(match.group())
            sent[1] = sent[1] + 0.05 * answer_pattern[1]
            answer_list.append(sent)

def keyword_matching(target):
    regexPattern = str()
    keywords = stop_words_elimination(target)
    for word in keywords:
        regexPattern = regexPattern + "(?=.*\s" + word + "\s)"
    for sent in sorted_sent_list:
        match = re.search(r'(' + regexPattern + ').*', sent[0], re.IGNORECASE)
        if match:
            # print(match.group())
            sent[1] = sent[1] + 0.01
            answer_list.append(sent)

def target_counting(target):
    count = list()
    regexPattern = target.replace(" ", "\s")
    for sent in sorted_sent_list:
        match = re.findall(r'(' + regexPattern + ')', sent[0], re.IGNORECASE)
        if(len(match)>1):
            sent[1] = sent[1] + 0.01 * len(match)
        count.append(len(match))
    return count

def target_lemma_counting(target):
    count = list()
    pattern = text_normalizing(target)
    regexPattern = pattern.replace(" ", "\s")
    for sent in sorted_sent_list:
        sent_words = text_normalizing(sent[0])
        match = re.findall(r'(' + regexPattern + ')', sent_words, re.IGNORECASE)
        if (len(match) > 1):
            sent[1] = sent[1] + 0.005 * len(match)
        count.append(len(match))
    return count

pattern1 = r"""Chunk: {<WP|WDT|WP$|WRB>?}"""
pattern2 = r"""Chunk: {<VB|VBD|VBG|VBN|VBP|VBZ>*}"""
pattern3 = r"""Chunk: {<DT|JJ|JJR|JJS|NN|NNS|NNP|NNPS>*}"""
pattern4 = r"""Chunk: {<IN|DT|JJ|JJR|JJS|NN|NNS|NNP|NNPS>*}"""

question_word = question_segmenting(query_sentence, pattern1)
verb = question_segmenting(query_sentence, pattern2)
target = question_segmenting(query_sentence, pattern4)
compliment = question_segmenting(query_sentence, pattern4)


answer_pattern_1 = (query_sentence, 5)
answer_pattern_2 = (target + " " + verb + " defined as", 4)
answer_pattern_3 = (verb + " defined as " + target, 4)
answer_pattern_4 = (" definition of " + target, 4)
answer_pattern_5 = (target + " " + verb, 0.75)
answer_pattern_6 = (target, 0.1)


list_of_answer_patterns = (answer_pattern_1, answer_pattern_2, answer_pattern_3, answer_pattern_4, answer_pattern_5, answer_pattern_6)
#
for pattern in list_of_answer_patterns:
    answer_pattern_matching(pattern)
    if not answer_list:
        pattern_lemma_matching(pattern)
        if not answer_list:
            keyword_matching(target)

# answer_pattern_matching(answer_pattern_1)
# pattern_lemma_matching(answer_pattern_1)

# target_counting(target)
# target_lemma_counting(target)
# keyword_matching(target)

# print(formatted_query)
# print(target)
# print("target count: " + str(target_counting(target)))
# print("target lemma count: " + str(target_lemma_counting(target)))
# print(keyword_matching(target))

answer_list_new = set(tuple(answer) for answer in answer_list)
sorted_answer_list = sorted((doc for doc in answer_list_new), key=operator.itemgetter(1), reverse = True)


# for sent in sorted_answer_list:
#     print(sent)
print(sorted_answer_list[0][0])
print("----------line separator----------")
# for i in sorted_sent_list:
#     print(i)
