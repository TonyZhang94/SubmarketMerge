# -*- coding:utf-8 -*-


from SubmarketMerge.settings import Parameters, FileBase
from SubmarketMerge.tools.public import Entrance
from SubmarketMerge.tools.knowledge import knowledge_country
from SubmarketMerge.tools.utils import load, dump


class ShowMethod(object):
    def __init__(self):
        """Init"""

    def show(self):
        """Show Function"""
        raise NotImplementedError

    @staticmethod
    def load(name):
        pcid, cid, _ = Entrance().params
        return load(_, FileBase.result.format(pcid=pcid, cid=cid, name=name))

    @staticmethod
    def dump(data, name):
        pcid, cid, _ = Entrance().params
        dump(data, _, repath=FileBase.result.format(pcid=pcid, cid=cid, name=name))


class ShowPairWordsMethod(ShowMethod):
    """Show Words (Append Country And Other Knowledge) As Pair"""
    def __init__(self):
        self.threshold = Parameters.addAddAllCountryPairFlag

    def show(self):
        mapping = load("smMapping")
        info = super().load("submarketInfo")
        _, _, country_map = knowledge_country()
        for _, country_words in country_map.items():
            country = set()
            for country_word in country_words:
                if info[country_word]["inTitle"] or self.threshold:
                    country.add(country_word)
            for word1 in country:
                for word2 in country:
                    if word1 == word2:
                        continue
                    if len(word1) > len(word2):
                        w1, w2 = word2, word1
                    elif len(word1) == len(word2) and word1 > word2:
                        w1, w2 = word2, word1
                    else:
                        w1, w2 = word1, word2
                    mapping.add((w1, w2))
        super().dump(mapping, "smMapping")


class ShowSetWordsMethod(ShowMethod):
    """Show Words (Append Country And Other Knowledge) As Set"""
    def __init__(self):
        self.threshold = Parameters.addAddAllCountrySetFlag

    def show(self):
        keep = load("smKeep")
        info = super().load("submarketInfo")
        _, _, country_map = knowledge_country()
        for _, country_words in country_map.items():
            country = set()
            for country_word in country_words:
                if info[country_word]["inTitle"] or self.threshold:
                    country.add(country_word)
            if len(country) >= 2:
                keep.append(country)
        super().dump(keep, "smKeep")


class ShowTopWordsMethod(ShowMethod):
    """Show Top Biz30day & Total Sold Price Words"""
    def __init__(self):
        self.threshold = {
            "biz top num": Parameters.showWordsBizTopNum,
            "sold top num": Parameters.showWordsSoldTopNum
        }

    def show(self):
        biz_rerank = load("statsAllSubBiz30dayReRank")
        sold_rerank = load("statsAllSubTotalSoldPriceReRank")

        biz_top_words, num = list(), 0
        for rank in range(1, self.threshold["biz top num"]+1):
            try:
                words = biz_rerank[rank]
            except KeyError:
                print("Don't have enough words as expect.")
                break
            if num < self.threshold["biz top num"]:
                biz_top_words.extend(words)
                num += len(words)
            else:
                break

        sold_top_words, num = list(), 0
        for rank in range(1, self.threshold["sold top num"]+1):
            try:
                words = sold_rerank[rank]
            except KeyError:
                print("Don't have enough words as expect.")
                break
            if num < self.threshold["sold top num"]:
                sold_top_words.extend(words)
                num += len(words)
            else:
                break

        super().dump(biz_top_words, "topBizWords")
        super().dump(sold_top_words, "topSoldWords")


class ShowTopWordsExceptKeepWordsMethod(ShowMethod):
    """Show Top Biz30day & Total Sold Price Words Which Not Included In Keep"""
    def __init__(self):
        self.threshold = {
            "biz top num": Parameters.showWordsExceptKeepWordsBizTopNum,
            "sold top num": Parameters.showWordsExceptKeepWordsSoldTopNum
        }

    def show(self):
        biz_rerank = load("statsAllSubBiz30dayReRank")
        sold_rerank = load("statsAllSubTotalSoldPriceReRank")
        keep = super().load("smKeep")
        all_keep_words = set()
        for words in keep:
            all_keep_words |= words

        biz_top_words, rank, num = list(), 0, 0
        while True:
            rank += 1
            try:
                words = biz_rerank[rank]
            except KeyError:
                print("Don't have enough words as expect.")
                break
            if num < self.threshold["biz top num"]:
                for word in words:
                    if word not in all_keep_words:
                        biz_top_words.append(word)
                        num += 1
            else:
                break

        sold_top_words, num = list(), 0
        while True:
            rank += 1
            try:
                words = sold_rerank[rank]
            except KeyError:
                print("Don't have enough words as expect.")
                break
            if num < self.threshold["sold top num"]:
                for word in words:
                    if word not in all_keep_words:
                        sold_top_words.append(word)
                        num += 1
            else:
                break

        super().dump(biz_top_words, "topBizWordsExceptKeepWords")
        super().dump(sold_top_words, "topSoldWordsExceptKeepWords")
