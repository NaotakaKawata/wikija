import xml.etree.ElementTree as ET
import sys
from sys import argv
import os
import MeCab
import re
import pickle
import json
from flask import Flask, render_template
app = Flask(__name__) #インスタンス生成




def read_json(filename):
    with open(filename) as f:
        jsonfile = json.load(f)
    return jsonfile

def concat_morpheme(dic):
    sentence_list = []
    link_list = []
    tag_list = []
    sentence_lists = []
    link_lists = []
    tag_lists = []
    sentence = ""
    link = ""
    tag = ""
    link_count = 0
    for i in range(len(dic["ner"]["sentences"])):
        link_count = 0
        sentence_list = []
        link_list = []
        tag_list = []
        for j in range(len(dic["ner"]["sentences"][i])):
            if dic["ner"]["tags"][i][j].startswith("B-"):
                sentence += dic["ner"]["sentences"][i][j]
                link = dic["ner"]["linked"][i][link_count]["title"]

                tag = dic["ner"]["extracted"][i][link_count][1]
                link_count += 1
            elif dic["ner"]["tags"][i][j].startswith("I-"):
                sentence += dic["ner"]["sentences"][i][j]
            else:
                if sentence != "":
                    sentence_list.append(sentence)
                    link_list.append(link)
                    tag_list.append(tag)
                    sentence = ""
                    link = ""
                    tag = ""
                sentence_list.append(dic["ner"]["sentences"][i][j])
                link_list.append("")
                tag_list.append("")
        if sentence != "":
            sentence_list.append(sentence)
            link_list.append(link)
            tag_list.append(tag)
            sentence = ""
            link = ""
            tag = ""
        sentence_lists.append(sentence_list)
        link_lists.append(link_list)
        tag_lists.append(tag_list)
    #print(sentence_lists)
    #print(link_lists)
    #print(tag_lists)
    return sentence_lists, link_lists, tag_lists

@app.route("/") 
def index():
    list = []
    datas = []
    data = {}

    predict_path = 'output.json'
    predict = read_json(predict_path)
    sentence_lists, link_lists, tag_lists = concat_morpheme(predict)
    for i in range(len(sentence_lists)):
        for j in range(len(sentence_lists[i])):
            data["morpheme"] = sentence_lists[i][j]
            if link_lists[i][j] != "" :
                data["url"] = " https://ja.wikipedia.org/?curid=" + link_lists[i][j]
                data["tag"] = tag_lists[i][j]
            else:
                data["url"] = ""
                data["tag"] = ""
            datas.append(data)
            data = {}
        list.append(datas)
        datas = []

    return render_template('index.html', datas=list) #/indexにアクセスが来たらtemplates内のindex.htmlが開きます
#ここがサーバーサイドからクライアントサイドへなにかを渡すときのポイントになります。

if __name__ == "__main__":
    #predict_path = 'output.json'
    #predict = read_json(predict_path)
    #concat_morpheme(predict)
    #print(predict)
    # webサーバー立ち上げ

    app.run()
    exit(0)
