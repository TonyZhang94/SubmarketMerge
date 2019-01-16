# -*- coding:utf-8 -*-

import os
import importlib

from SubmarketMerge.settings import Mode
from SubmarketMerge.tools.public import Descriptor

from SubmarketMerge.component.initMethod import *
from SubmarketMerge.component.cutMethod import *
from SubmarketMerge.component.mergeMethod import *
from SubmarketMerge.component.eraseMethod import *
from SubmarketMerge.component.pairMethod import *
from SubmarketMerge.component.appendMethod import *
from SubmarketMerge.component.statisticMethod import *
from SubmarketMerge.component.buildInfoMethod import *
from SubmarketMerge.component.transMethod import *
from SubmarketMerge.component.clearFileMethod import *

# try:
#     modules = [importlib.import_module(".", "component." + module.replace(".py", ""))
#                for module in os.listdir("component/")
#                if "__" not in module and module not in ["taskObj"]]
#     for module in modules:
#         print(module.__name__)
#         __import__(module.__name__, *)
# except ModuleNotFoundError as e:
#     raise e


class TasksObj(object):
    """Tasks Obj Base Class"""
    def __init__(self, *args, **kwargs):
        """Init Function"""

    def execute(self):
        """Excute Commands"""


class InitCommand(TasksObj):
    obj = Descriptor(InitMethod)

    def __init__(self, method):
        self.obj = method()

    @logging
    def execute(self):
        self.obj.init()


class CutCommand(TasksObj):
    obj = Descriptor(CutMethod)

    def __init__(self, method, threshold=None):
        if Mode.cutLOCAL or method is None:
            self.obj = UseLocalCutMethod(method)
        else:
            self.obj = method()

        if threshold is not None:
            self.obj.threshold = threshold

        if hasattr(self.obj, "threshold"):
            self.doc = self.obj.__doc__ + " // Threshold " + str(self.obj.threshold)

    @logging
    def execute(self):
        self.obj.cut()


class MergeCommand(TasksObj):
    obj = Descriptor(MergeMethod)

    def __init__(self, method):
        self.obj = method()

    @logging
    def execute(self):
        self.obj.merge()


class EraseCommand(TasksObj):
    obj = Descriptor(EraseMethod)

    def __init__(self, method, threshold=None):
        self.obj = method()
        if threshold is not None:
            self.obj.threshold = threshold

        if hasattr(self.obj, "threshold"):
            self.doc = self.obj.__doc__ + " // Threshold " + str(self.obj.threshold)

    @logging
    def execute(self):
        self.obj.erase()


class PairCommand(TasksObj):
    obj = Descriptor(PairMethod)

    def __init__(self, method, threshold=None):
        self.obj = method()
        if threshold is not None:
            self.obj.threshold = threshold

        if hasattr(self.obj, "threshold"):
            self.doc = self.obj.__doc__ + " // Threshold " + str(self.obj.threshold)

    @logging
    def execute(self):
        self.obj.pair()


class AppendCommand(TasksObj):
    obj = Descriptor(AppendMethod)

    def __init__(self, method):
        self.obj = method()

    @logging
    def execute(self):
        self.obj.append()


class StatisticCommand(TasksObj):
    obj = Descriptor(StatisticMethod)

    def __init__(self, method):
        if Mode.statsLOCAL or method is None:
            self.obj = UseLocalStatsMethod(method)
        else:
            self.obj = method()

    @logging
    def execute(self):
        self.obj.statistic()


class BuildInfoCommand(TasksObj):
    obj = Descriptor(BuildInfoMethod)

    def __init__(self, method, threshold=None):
        self.obj = method()
        if threshold is not None:
            self.obj.threshold = threshold

        if hasattr(self.obj, "threshold"):
            self.doc = self.obj.__doc__ + " // Threshold " + str(self.obj.threshold)

    @logging
    def execute(self):
        self.obj.build()


class TransCommand(TasksObj):
    obj = Descriptor(TransMethod)

    def __init__(self, method):
        self.obj = method()

    @logging
    def execute(self):
        self.obj.trans()


class ClearFileCommand(TasksObj):
    obj = Descriptor(ClearFileMethod)

    def __init__(self, method):
        if Mode.clearLOCAL or method is None:
            self.obj = method()
        else:
            self.obj = ClearNothingMethod()

    @logging
    def execute(self):
        self.obj.clear()
