# -*- coding:utf-8 -*-


from SubmarketMerge.tools.utils import load, dump


class TransMethod(object):
    def __init__(self):
        """Init"""

    def trans(self):
        """Trans Function"""


class SetTransToPairMethod(TransMethod):
    """Transform Relationship From Set To Pair"""
    def trans(self):
        keep = load("smKeep")

        mapping = set()
        for key, words in keep.items():
            key_and_words = words
            key_and_words.add(key)
            for word1 in key_and_words:
                for word2 in key_and_words:
                    if word1 == word2:
                        continue
                    if len(word1) > len(word2):
                        w1, w2 = word2, word1
                    elif len(word1) == len(word2) and word1 > word2:
                        w1, w2 = word2, word1
                    else:
                        w1, w2 = word1, word2
                    mapping.add((w1, w2))

        dump(mapping, "smMapping")


class PairTransToSetMethod(TransMethod):
    """Transform Relationship From Pair To Set"""
    def trans(self):
        mapping = load("smMapping")
        keep_set = list()
        for pair in mapping:
            keep_set.append(set(pair))

        while True:
            temp_keep_set = list()
            for words in keep_set:
                merge_flag = False
                for merge_words in temp_keep_set:
                    if 0 != len(words & merge_words):
                        merge_words |= words
                        merge_flag = True
                if not merge_flag:
                    temp_keep_set.append(words)
            if keep_set == temp_keep_set:
                break
            keep_set = temp_keep_set

        dump(keep_set, "smKeep")
