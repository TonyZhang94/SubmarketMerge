# -*- coding:utf-8 -*-

import jieba.analyse

from SubmarketMerge.tools.utils import load, dump, clear_brand, read
from SubmarketMerge.component.readData import *


class CutMethod(object):
    """Cut Method"""
    def __init__(self):
        """Init"""

    def cut(self):
        """Cut Function"""
        raise NotImplementedError


class CutWithBrandMethod(CutMethod):
    """Cut Top Trending Searches And Title With Brand"""
    def __init__(self):
        self.threshold = {
            "title": Parameters.cutTitleWordsNum,
            "hot search": Parameters.cutHotSearchWordsNum
        }

    def cut(self):
        df = read("factItem")()
        title = "".join(list(df['title']))
        cut_word = jieba.analyse.textrank(title, topK=self.threshold["title"])
        title_words = set()
        for i, word in enumerate(list(cut_word)):
            title_words.add(word)
        dump(title_words, "titleHotWords")

        df = read("hotWords")()
        title = "".join(list(df['hotwords']))
        cut_word = jieba.analyse.textrank(title, topK=self.threshold["hot search"])
        search_words = set()
        for i, word in enumerate(list(cut_word)):
            search_words.add(word)
        dump(search_words, "searchHotWords")


class CutWithoutBrandMethod(CutMethod):
    def __init__(self):
        self.threshold = {
            "title": Parameters.cutTitleWordsNum,
            "hot search": Parameters.cutHotSearchWordsNum
        }

    """Cut Top Trending Searches And Title Without Brand"""
    def cut(self):
        df = read("factItem")()
        for k, v in df.iterrows():
            df.at[k, "title"] = clear_brand(v["title"], v["brand"])
        title = "".join(list(df['title']))
        cut_word = jieba.analyse.textrank(title, topK=self.threshold["title"])
        title_words = set()
        for i, word in enumerate(list(cut_word)):
            title_words.add(word)
        dump(title_words, "titleHotWords")

        df = read("hotWords")()
        title = "".join(list(df['hotwords']))
        cut_word = jieba.analyse.textrank(title, topK=self.threshold["hot search"])
        search_words = set()
        for i, word in enumerate(list(cut_word)):
            search_words.add(word)
        dump(search_words, "searchHotWords")


class UseLocalCutMethod(CutMethod):
    """Use Local Files As The Result Of Cut Method"""
    def __init__(self, method):
        self.threshold = {
            "title": Parameters.cutTitleWordsNum,
            "hot search": Parameters.cutHotSearchWordsNum
        }
        self.method = method

    def cut(self):
        try:
            load("titleHotWords")
            load("searchHotWords")
        except FileNotFoundError:
            self.method().cut()
        except Exception as e:
            raise e
