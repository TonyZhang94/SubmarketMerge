# -*- coding:utf-8 -*-


from word_similarity import WordSimilarity2010

from SubmarketMerge.settings import Parameters
from SubmarketMerge.tools.knowledge import common_char
from SubmarketMerge.tools.utils import load, dump


class PairMethod(object):
    def __init__(self):
        """Init"""

    def pair(self):
        """Pair Function"""
        raise NotImplementedError

    @staticmethod
    def load():
        return load("submarketWords"), load("smKeep"), load("smDrop"), load("smMapping")

    @staticmethod
    def dump(words, keep, drop, mapping):
        dump(words, "submarketWords")
        dump(keep, "smKeep")
        dump(drop, "smDrop")
        dump(mapping, "smMapping")


class PairWholeSemanticsMethod(PairMethod):
    """Make Similar Pair Through Whole Semantics Of Words"""
    def __init__(self):
        self.threshold = Parameters.wholeSemanticsThreshold

    def pair(self):
        words, keep, drop, mapping = super().load()
        ws_tool = WordSimilarity2010()
        common_chars = common_char()

        for word1 in words:
            for word2 in words:
                if word1 == word2:
                    continue
                sim = ws_tool.similarity(word1, word2)
                if sim >= self.threshold:
                    if len(word1) > len(word2):
                        w1, w2 = word2, word1
                    elif len(word1) == len(word2) and word1 > word2:
                        w1, w2 = word2, word1
                    else:
                        w1, w2 = word1, word2
                    if 0 != len(set(w1) & common_chars) \
                            and 0 != len(set(w2) & common_chars):
                        # print("they are not similar words", w1, w2)
                        continue
                    mapping.add((w1, w2))
                    keep.setdefault(w1, set()).add(w2)
                    keep.setdefault(w2, set()).add(w1)

        super().dump(words, keep, drop, mapping)


class PairLiteralContainMethod(PairMethod):
    """Make Similar Pair Through Relationships Of Literal Contain"""
    def pair(self):
        words, keep, drop, mapping = super().load()
        for word1 in words:
            for word2 in words:
                if word1 == word2:
                    continue
                if word1 in word2 or word2 in word1:
                    if word1 in word2:
                        w1, w2 = word1, word2
                    else:
                        w1, w2 = word2, word1
                        mapping.add((w1, w2))
                    keep.setdefault(w1, set()).add(w2)
                    keep.setdefault(w2, set()).add(w1)

        super().dump(words, keep, drop, mapping)


class PairEditDistanceMethod(PairMethod):
    """Make Similar Pair Through Edit Distance Of Words"""
    def __init__(self):
        self.threshold = Parameters.pairIntersectionEditDistanceThreshold

    def pair(self):
        words, keep, drop, mapping = super().load()
        common_chars = common_char()
        ws_tool = WordSimilarity2010()

        visit = set()
        for word1 in list(words):
            for word2 in list(words):
                if word1 == word2:
                    continue
                if len(word1) > len(word2):
                    w1, w2 = word2, word1
                elif len(word1) == len(word2) and word1 > word2:
                    w1, w2 = word2, word1
                else:
                    w1, w2 = word1, word2
                if (w1, w2) in visit:
                    continue
                visit.add((w1, w2))
                chars = set(w1)
                for char in chars:
                    if char in common_chars:
                        continue
                    if char in w2 and len(w1) == len(w2):
                        sim = ws_tool.similarity(w1, w2)
                        if sim < self.threshold:
                            continue
                        mapping.add((w1, w2))
                        keep.setdefault(w1, set()).add(w2)
                        keep.setdefault(w2, set()).add(w1)

        super().dump(words, keep, drop, mapping)


class PairReverseMethod(PairMethod):
    """Make Similar Pair Through Reverse String"""
    def pair(self):
        words, keep, drop, mapping = super().load()
        for word1 in words:
            for word2 in words:
                if word1 == word2:
                    continue
                w1, w2 = word1, word2[:: -1]
                if w1 != w2:
                    continue
                if word1 > word2:
                    w1, w2 = word2, word1
                else:
                    w1, w2 = word1, word2
                mapping.add((w1, w2))
                keep.setdefault(w1, set()).add(w2)
                keep.setdefault(w2, set()).add(w1)

        super().dump(words, keep, drop, mapping)
