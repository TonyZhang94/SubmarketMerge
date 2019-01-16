# -*- coding:utf-8 -*-

from DBparam import *
from SubmarketMerge.tools.myExceptions import *

# class Outer99(object):
#     host = $ip$
#     port = $port$
#     user = $username$
#     password = $password$
#
#     DB = dict()
#     DB["standard_library"] = "standard_library"
#     DB["fact_library"] = "fact_library"
#     DB["zhuican_web"] = "zhuican_web"
#     DB["raw_mj_category"] = "raw_mj_category"
#     DB["report_dg"] = "report_dg"
#     DB["raw_tb_comment_notag"] = "raw_tb_comment_notag"


# DBDefault = Outer99
DBDefault = DB99


class Mode(object):
    """For Test"""
    srcLOCAL = True
    cutLOCAL = True
    savePKL = True
    statsLOCAL = True
    # statsLOCAL = False
    # clearLOCAL = True
    clearLOCAL = False

    """For Use"""
    # stcLOCAL = True
    # cutLOCAL = False
    # statsLOCAL = False
    # savePKL = True
    # clearLOCAL = True

    def __new__(cls, *args, **kwargs):
        raise InstantiationError


class Parameters(object):
    cutTitleWordsNum = 300
    cutHotSearchWordsNum = 300

    cidnameSimThreshold = 0.7

    coBrandFilterNum = 20
    enBrandFilterNum = 20
    zhBrandFilterNum = 500

    wholeSemanticsThreshold = 0.9
    pairIntersectionEditDistanceThreshold = 0
    pairUnionEditDistanceThreshold = 0.4

    mainBizThreshold = 0.8
    topBizNum = 20
    mainSoldThreshold = 0.8
    topSoldNum = 20

    def __new__(cls, *args, **kwargs):
        raise InstantiationError


class FileBase(object):
    info = "data/info_{name}_pcid{pcid}cid{cid}.csv"
    infoPath = "data/"

    temporary = "temporary/pcid{pcid}cid{cid}/{name}.pkl"
    temporaryPath = "temporary/pcid{pcid}cid{cid}/"

    result = "result/pcid{pcid}cid{cid}/{name}.pkl"
    resultPath = "result/pcid{pcid}cid{cid}/"

    crossPcidPath = "cross_pcid/pcid{pcid}final.csv"

    history = "tools/history.pkl"

    def __new__(cls, *args, **kwargs):
        raise InstantiationError


class EraseWords(object):
    eraseWords = dict()

    wrong_all = []

    items = []
    items.extend(wrong_all)
    # eraseWords["4 50012097"] = set(items)
    eraseWords["2 50008881"] = set(items)

    def __new__(cls, *args, **kwargs):
        raise InstantiationError


class AppendWords(object):
    appendWords = dict()

    append_all = []

    items = []
    items.extend(append_all)
    # eraseWords["4 50012097"] = set(items)
    appendWords["2 50008881"] = set(items)

    def __new__(cls, *args, **kwargs):
        raise InstantiationError


if __name__ == '__main__':
    try:
        m = Mode()
    except Exception as e:
        print(e)
