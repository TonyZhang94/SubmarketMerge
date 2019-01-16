# -*- coding:utf-8 -*-

import os

from SubmarketMerge.settings import FileBase
from SubmarketMerge.tools.public import Entrance
from SubmarketMerge.tools.utils import *


class InitMethod(object):
    """Init Method"""
    def __init__(self):
        """Init"""

    def init(self):
        """Init Function"""


class InitFilesMethod(InitMethod):
    """Initialize Directory And Files For Processing"""
    def init(self):
        pcid, cid, _ = Entrance().params
        try:
            os.makedirs("data")
        except FileExistsError:
            pass
        except Exception as e:
            raise e

        try:
            os.makedirs(FileBase.temporaryPath.format(pcid=pcid, cid=cid))
        except FileExistsError:
            pass
        except Exception as e:
            raise e

        try:
            os.makedirs(FileBase.resultPath.format(pcid=pcid, cid=cid))
        except FileExistsError:
            pass
        except Exception as e:
            raise e

        try:
            dump(dict(), "smKeep")
            dump(set(), "smDrop")
            dump(set(), "smMapping")
        except Exception as e:
            raise e

