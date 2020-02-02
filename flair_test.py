from flair.data import Sentence
from flair.models import SequenceTagger
from collections import defaultdict
import json
import MeCab

def make_wakati(filename):
    text = []
    result = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        sentences = file.read()
    sentences = sentences.splitlines()
    mecab = MeCab.Tagger("-Owakati")
    mecab.parse('')
    for sentence in sentences:
        text = []
        word = ""
        if len(sentence) == 0:
            continue
        word = mecab.parse(sentence)
        word = word.rstrip(" \n")
        result.append(word)
    return result

def convert_flair(input):
    sentence = []
    tag = []
    list = input.split(" ")
    for line in list :
        if line.startswith("<B-") or line.startswith("<I-"):
            tag[-1] = line.strip('< >')
        else:
            sentence.append(line)
            tag.append("O")
    return sentence,tag

def convert_json(sentences,tags):
    dic = defaultdict(list)
    for i in range(len(sentences)):
        dic["sentences"].append(sentences[i])
        dic["tags"].append(tags[i])
    adjust_dic = {"ner" : dic}
    return adjust_dic

def add_offset(dic):
    sentence_length = 0
    start_offset = 0
    end_offset = 0
    sentence = ""
    tag = ""
    sentence_and_tag = []
    mention = []
    start = []
    end = []
    list_mention = []
    list_start = []
    list_end = []
    null_list = []
    proccessing_flag = False
    no_mention_flag = True

    for i in range(len(dic["ner"]["sentences"])):
        if no_mention_flag == True and i != 0:
            list_mention.append(null_list)
            list_start.append(null_list)
            list_end.append(null_list)
        elif no_mention_flag == False and i != 0:
            if proccessing_flag == True:
                end_offset = sentence_length
                sentence_and_tag.append(sentence)
                sentence_and_tag.append(tag)
                #mention.append(sentence)
                mention.append(sentence_and_tag)
                start.append(start_offset)
                end.append(end_offset)
            list_mention.append(mention)
            list_start.append(start)
            list_end.append(end)
        proccessing_flag = False
        no_mention_flag = True
        sentence = ""
        tag = ""
        mention = []
        start = []
        end = []
        start_offset = 0
        end_offset = 0

        for j in range(len(dic["ner"]["sentences"][i])):
            if dic["ner"]["tags"][i][j].startswith("B-"):
                no_mention_flag = False
                if proccessing_flag == True:
                    end_offset = sentence_length
                    sentence_and_tag.append(sentence)
                    sentence_and_tag.append(tag)
                    mention.append(sentence_and_tag)
                    start.append(start_offset)
                    end.append(end_offset)
                    start_offset = 0
                    end_offset = 0
                    proccessing_flag = False
                    sentence = ""
                    tag = ""
                    sentence_and_tag = []

                proccessing_flag = True
                sentence += dic["ner"]["sentences"][i][j]
                tag = dic["ner"]["tags"][i][j].lstrip("B-")
                start_offset = sentence_length + 1

            elif dic["ner"]["tags"][i][j] == "O":
                if proccessing_flag == True:
                    end_offset = sentence_length
                    sentence_and_tag.append(sentence)
                    sentence_and_tag.append(tag)
                    mention.append(sentence_and_tag)
                    start.append(start_offset)
                    end.append(end_offset)
                    start_offset = 0
                    end_offset = 0
                    proccessing_flag = False
                    sentence = ""
                    tag = ""
                    sentence_and_tag = []
            elif dic["ner"]["tags"][i][j].startswith("I-"):
                sentence += dic["ner"]["sentences"][i][j]
            sentence_length += len(dic["ner"]["sentences"][i][j])
            sentence_length -= dic["ner"]["sentences"][i][j].count("　")

    if no_mention_flag == True:
        list_mention.append(null_list)
        list_start.append(null_list)
        list_end.append(null_list)
    elif no_mention_flag == False:
        list_mention.append(mention)
        list_start.append(start)
        list_end.append(end)
    for i in range(len(list_mention)):
        dic["ner"]["extracted"].append(list_mention[i])
        dic["ner"]["start_offset"].append(list_start[i])
        dic["ner"]["end_offset"].append(list_end[i])
    return dic

def write_json(filename, dic):
    json_file = open(filename, 'w')
    json.dump(dic, json_file, ensure_ascii=False)
    return

if __name__ == '__main__':
    test_path = 'input.txt'
    result_path = 'predict.json'
    model = SequenceTagger.load('output/best-model.pt')
    input_sentences = []
    sentences = []
    tags = []

    file = make_wakati(test_path)
    for i in range(len(file)):
        line = file[i]
        input_sentence = Sentence(line)
        model.predict(input_sentence)
        input_sentences.append(input_sentence)
    for line in input_sentences:
        sentence, tag = convert_flair(line.to_tagged_string())
        sentences.append(sentence)
        tags.append(tag)
    predict_dictionary = convert_json(sentences, tags)
    predict_dictionary = add_offset(predict_dictionary)
    write_json(result_path, predict_dictionary)
