# -*- coding:utf-8 -*-


from SubmarketMerge.settings import AppendWords
from SubmarketMerge.tools.public import Entrance
from SubmarketMerge.tools.knowledge import knowledge_country
from SubmarketMerge.tools.utils import load, dump


class AppendMethod(object):
    def __init__(self):
        """Init"""

    def append(self):
        """Append Function"""
        raise NotImplementedError

    @staticmethod
    def load():
        return load("submarketWords")

    @staticmethod
    def dump(words):
        dump(words, "submarketWords")


class AppendSpecialMethod(AppendMethod):
    """Append Special Words For Special Pcid Cid"""
    def append(self):
        pcid, cid, _ = Entrance().params
        key = "%s %s" % (pcid, cid)
        if key not in AppendWords.appendWords.keys():
            return
        words = super().load()
        for word in AppendWords.appendWords[key]:
            words.add(word)
        super().dump(words)


class AppendCountryMethod(AppendMethod):
    """Append Country Words"""
    def append(self):
        words = super().load()
        country, _, _ = knowledge_country()
        super().dump(words | country)


class AppendKeepCountryMethod(AppendMethod):
    def append(self):
        pass
