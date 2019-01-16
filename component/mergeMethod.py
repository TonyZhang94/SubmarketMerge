# -*- coding:utf-8 -*-

from SubmarketMerge.tools.utils import load, dump


class MergeMethod(object):
    def __init__(self):
        """Init"""

    def merge(self):
        """Merget Function"""


class IntersectionMethod(MergeMethod):
    """Merge Submarket By Intersection"""
    def merge(self):
        title_words = load("titleHotWords")
        search_words = load("searchHotWords")
        words = title_words & search_words
        dump(words, "submarketWords")


class UnionMethod(MergeMethod):
    """Merge Submarket By Union"""
    def merge(self):
        title_words = load("titleHotWords")
        search_words = load("searchHotWords")
        words = title_words | search_words
        dump(words, "submarketWords")
