# -*- coding:utf-8 -*-


from SubmarketMerge.tools.public import Entrance

from SubmarketMerge.component.tasksObj import *
from SubmarketMerge.tools.utils import *


if __name__ == '__main__':
    pcid, cid, _ = Entrance(pcid="2", cid="50008881", datamonth="201810", cidname="文胸").params

    show("smDrop")
