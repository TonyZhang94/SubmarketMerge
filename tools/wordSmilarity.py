# -*- coding:utf-8 -*-
import re
import urllib
from urllib.request import Request, urlopen

import requests
import urllib3

import time
from bs4 import BeautifulSoup

url_model = "https://wordsimilarity.com/zh/"


DIRECTORY = "1"
interrupt = "selfies"  # 卡在哪个词不动选哪个词


class WordSimilarity:
    def __init__(self):
        self.useless_file = "public/useless.csv"
        self.keys_file = "/noun.csv"
        self.des = "/sim_value.csv"
        self.useless = set()
        self.key = list()
        self.records = dict()

        self.begin = False

    def match_one(self, start, end, text):
        head = text.index(start)
        tail = text.index(end)

        return text[head: tail]

    def match_all(self, start, end, text):
        suffix = len(end)
        tail = text.index(end)
        text = text[tail+suffix:]

        records = list()
        while True:
            try:
                head = text.index(start)
                tail = text.index(end)
                block = text[head: tail+suffix]
                records.append(self.match_one(start, end, block))
                text = text[tail+suffix:]
            except Exception as e:
                break

        return records

    def find_sim(self, line):
        inx = line.index("<a")
        line = line[inx:]
        head = line.index(">") + 1
        tail = line.index("</a>")
        return line[head: tail]

    def find_value(self, line):
        inx = line.index("</a>") + len("</a>")
        line = line[inx:]
        res = line.replace("&nbsp;", "").replace("'", "").strip()
        return res

    def process(self, key):
        url = url_model + urllib.parse.quote(key)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        try_time = 1
        while True:
            try:
                req = Request(url, headers=headers)
                response = urlopen(req)
                content = response.read()
                content = str(content, encoding='utf-8')
                break
            except Exception as e:
                print(e)
                print("try time", try_time)
                try_time += 1
                if 6 == try_time:
                    exit(0)

        div = self.match_one("十大相似词或者同义词", "三十大相近词或者同义词", content)
        lines = self.match_all("<p", "</p>", div)

        sim = list()
        value = list()
        for line in lines:
            sim.append(self.find_sim(line))
            value.append(float(self.find_value(line)))

        return sim, value

    def start(self, directory):
        words = open(self.useless_file).readlines()
        for word in words:
            self.useless.add(word.replace("\n", ""))

        lines = open(directory+self.keys_file).readlines()
        for line in lines:
            key = line.split(" ")[0]
            if key in self.useless:
                continue
            print(key)

            # interrupt
            if not self.begin:
                if interrupt == key:
                    self.begin = True
                else:
                    continue

            self.key.append(key)
            self.records[key] = dict()
            self.records[key]["sim"], self.records[key]["value"] = self.process(key)

            record = "{}: ".format(key)
            for inx in range(0, len(self.records[key]["sim"])):
                sim = self.records[key]["sim"][inx]
                value = self.records[key]["value"][inx]
                record += "{} {};".format(sim, value)
            writer = open(directory+self.des, 'ab')
            writer.writelines(record+"\n")
            writer.close()

            time.sleep(10)


if __name__ == '__main__':
    obj = WordSimilarity()
    obj.start(DIRECTORY)
