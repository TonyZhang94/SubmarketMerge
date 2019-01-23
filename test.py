# -*- coding:utf-8 -*-


from SubmarketMerge.tools.public import Entrance

from SubmarketMerge.component.tasksObj import *
from SubmarketMerge.tools.utils import *


if __name__ == '__main__':
    pcid, cid, _ = Entrance(pcid="2", cid="50008881", datamonth="201810", cidname="文胸").params

    # show("smDrop")
    # map1 = load("smMapping")
    # map2 = load("tempMapping")
    #
    # print(len(map1), len(map2))
    # if map1 == map2:
    #     print("一样")
    # else:
    #     print("不一样")
    #
    # for x in map2:
    #     if x not in map1:
    #         print(x)

    # for x in load("smKeep"):
    #     print(x)

    # show_word("日式")
    # show_word("钢圈")

    # rerank = load("statsSubBrandBizReRank")
    # for k, v in rerank["日式"].items():
    #     print(k, v)
