import re
import operator

from NLQProcessor import NLQprocessing
from textProcessor import pos_tagging, chunking, stop_words_elimination, stemming

def pattern_recognizer(query_sentence):

    answer_list = list()
    filtered_answers = list()
    sorted_sent_list = [list(sent) for sent in NLQprocessing(query_sentence)]

    def text_normalizing(text):
        words = stop_words_elimination(text)
        stems = stemming(words)
        string = " ".join(stem for stem in stems)
        return string

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
            match = re.search(r'(' + regexPattern + '\s)', sent[0], re.IGNORECASE)
            if match:
                print("Answer pattern matching successful")
                sent[1] = sent[1] + 0.2 * answer_pattern[1]
                answer_list.append(sent)

    def pattern_lemma_matching(answer_pattern):
        pattern = text_normalizing(answer_pattern[0])
        regexPattern = pattern.replace(" ", "\s")
        for sent in sorted_sent_list:
            sent_words = text_normalizing(sent[0])
            match = re.search(r'(' + regexPattern + '\s)', sent_words, re.IGNORECASE)
            if match:
                print("Pattern Lemma matching successful")
                sent[1] = sent[1] + 0.05 * answer_pattern[1]
                answer_list.append(sent)

    def keyword_matching(target):
        regexPattern = str()
        keywords = stop_words_elimination(target)
        for word in keywords:
            regexPattern = regexPattern + "(?=.*" + word + "\s)"
        for sent in sorted_sent_list:
            temp = stop_words_elimination(sent[0])
            temp = " ".join(s for s in temp)
            match = re.search(r'(' + regexPattern + '\s).*', temp, re.IGNORECASE)
            if match:
                print("Keywords matching successful")
                sent[1] = sent[1] + 0.01
                answer_list.append(sent)

    def target_counting(target):
        count = list()
        regexPattern = target.replace(" ", "\s")
        for sent in sorted_sent_list:
            match = re.findall(r'(' + regexPattern + '\s)', sent[0], re.IGNORECASE)
            if(len(match)>1):
                print("Target count: " + str(len(match)))
                sent[1] = sent[1] + 0.01 * len(match)
            count.append(len(match))
        return count

    def target_lemma_counting(target):
        count = list()
        pattern = text_normalizing(target)
        regexPattern = pattern.replace(" ", "\s")
        for sent in sorted_sent_list:
            sent_words = text_normalizing(sent[0])
            match = re.findall(r'(' + regexPattern + '\s)', sent_words, re.IGNORECASE)
            if (len(match) > 1):
                print("Target Lemma count: " + str(len(match)))
                sent[1] = sent[1] + 0.005 * len(match)
            count.append(len(match))
        return count

    def target_distance_counting(target):
        target = text_normalizing(target)
        regexPattern = target.replace(" ", "\s")
        for answer in answer_list:
            normalized_sent = text_normalizing(answer[0])
            match = re.split(r'(' + regexPattern + '\s)', normalized_sent, re.IGNORECASE)
            if(len(match)>1):
                proximity = (len(normalized_sent.split()) - len(match[0].split()))/len(normalized_sent.split())
                answer[1] = answer[1] + 1 * proximity
                # answer_list.append(sent)



    pattern1 = r"""Chunk: {<WP|WDT|WP$|WRB>?}"""
    pattern2 = r"""Chunk: {<VB|VBD|VBG|VBN|VBP|VBZ>.?}"""
    pattern3 = r"""Chunk: {<DT|JJ|JJR|JJS|NN|NNS|NNP|NNPS>*}"""
    pattern4 = r"""Chunk: {<IN|DT|JJ|JJR|JJS|NN|NNS|NNP|NNPS>*}"""

    question_word = question_segmenting(query_sentence, pattern1)
    verb = question_segmenting(query_sentence, pattern2)
    target = question_segmenting(query_sentence, pattern4)
    compliment = question_segmenting(query_sentence, pattern4)

    match = re.split(r'(' + verb + '\s)', query_sentence, re.IGNORECASE)
    target = match[2]
    print(target)
    print(verb)

    answer_pattern_1 = (query_sentence, 5)
    answer_pattern_2 = (target + " " + verb + " defined as", 4)
    answer_pattern_3 = (verb + " defined as " + target, 4)
    answer_pattern_4 = (" definition of " + target, 4)
    answer_pattern_5 = (target + " " + verb, 0.75)
    answer_pattern_6 = (target, 0.1)



    list_of_answer_patterns = (answer_pattern_1,answer_pattern_2,answer_pattern_3,answer_pattern_4,answer_pattern_5, answer_pattern_6)

    # for sent in sorted_sent_list:
    #     sent[1] = 0

    for pattern in list_of_answer_patterns:
        answer_pattern_matching(pattern)


    for pattern in list_of_answer_patterns:
        pattern_lemma_matching(pattern)


    keyword_matching(target)

    target_counting(target)
    target_lemma_counting(target)
    target_distance_counting(target)

    # answer_pattern_matching(answer_pattern_1)
    # pattern_lemma_matching(answer_pattern_1)

    # target_counting(target)
    # target_lemma_counting(target)
    # keyword_matching(target)

    # print("target count: " + str(target_counting(target)))
    # print("target lemma count: " + str(target_lemma_counting(target)))
    # print(keyword_matching(target))

    answer_set = set(tuple(answer) for answer in answer_list)
    sorted_answer_list = sorted((doc for doc in answer_set), key=operator.itemgetter(1), reverse = True)

    for answer in sorted_answer_list:
        filtered_answers.append(answer[0])

    # print("----------line separator----------")
    # if sorted_answer_list:
    #     print(sorted_answer_list[0][0])
    # print("----------line separator----------")
    # for sent in sorted_answer_list:
    #     print(sent)
    # for i in sorted_sent_list:
    #     print(i)
    return filtered_answers

