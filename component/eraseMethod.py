# -*- coding:utf-8 -*-

import pandas as pd

from SubmarketMerge.settings import EraseWords, FileBase, Parameters
from SubmarketMerge.tools.utils import load, dump
from SubmarketMerge.tools.public import Entrance
from SubmarketMerge.tools.knowledge import *
from SubmarketMerge.tools.wordSmilarity import *


class EraseMethod(object):
    def __init__(self):
        """Init"""

    def erase(self):
        """Erase Function"""
        raise NotImplementedError

    @staticmethod
    def load():
        return load("submarketWords"), load("smDrop")

    @staticmethod
    def dump(words, drops):
        dump(words, "submarketWords")
        dump(drops, "smDrop")


class EraseSpecialMethod(EraseMethod):
    """Erase Special Words For Special Pcid Cid"""
    def erase(self):
        pcid, cid, _ = Entrance().params
        key = "%s %s" % (pcid, cid)
        if key not in EraseWords.eraseWords.keys():
            return
        words, drop = super().load()
        for word in words:
            if word in EraseWords.eraseWords[key]:
                drop.add(word)
        super().dump(words-drop, drop)


class EraseCidnameSimMethod(EraseMethod):
    """Erase Cidname And Its Similar Words"""
    def __init__(self):
        self.threshold = Parameters.cidnameSimThreshold

    def erase(self):
        words, drop = super().load()
        try:
            history = load("history", FileBase.history)
        except FileNotFoundError:
            history = dict()

        cidname = Entrance().cidname
        if cidname in history.keys():
            sim_words, values = history[cidname]
        else:
            print("request ...")
            sim_words, values = WordSimilarity().process(cidname)
            history[cidname] = [sim_words, values]
            dump(history, "history", repath=FileBase.history)
        for word in words:
            for sim_word, sim in zip(sim_words, values):
                if sim_word in word and sim > self.threshold:
                    drop.add(word)
        drop.add(cidname)
        super().dump(words, drop)


class EraseCounryMethod(EraseMethod):
    """Erase Country Words"""
    def erase(self):
        words, drop = super().load()
        country, _, _ = knowledge_country()
        drop |= (words & country)
        words -= country
        super().dump(words, drop)


class EraseUselessMethod(EraseMethod):
    """Erase Useless Words"""
    def erase(self):
        words, drop = super().load()
        useless_words = knowledge_useless()
        for word in words:
            for useless_word in useless_words:
                if useless_word in word:
                    drop.add(word)
        super().dump(words-drop, drop)


class EraseBrandMethod(EraseMethod):
    """Erase Brand Words"""
    def __init__(self):
        self.threshold = {
            "co brand": Parameters.coBrandFilterNum,
            "en brand": Parameters.enBrandFilterNum,
            "zh brand": Parameters.zhBrandFilterNum
        }

    def erase(self):
        words, drop = super().load()
        pcid, _, _ = Entrance().params
        cross_pcid = pd.read_csv(FileBase.crossPcidPath.format(pcid=pcid))
        co = set(cross_pcid[cross_pcid["num"] > self.threshold["co brand"]]["brand"].values)
        en = set(cross_pcid[cross_pcid["num"] > self.threshold["en brand"]]["en"].values)
        zh = set(cross_pcid[cross_pcid["num"] > self.threshold["zh brand"]]["zh"].values)
        # for co_brand in co:
        #     try:
        #         en_brand, zh_brand = co_brand.split("/")
        #     except (ValueError, AttributeError):
        #         pass
        #     else:
        #         en.add(en_brand)
        #         zh.add(zh_brand)
        for word in words:
            if word in co or word in en or word in zh:
                drop.add(word)
        super().dump(words-drop, drop)
