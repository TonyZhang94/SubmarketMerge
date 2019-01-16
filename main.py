# -*- coding:utf-8 -*-

from SubmarketMerge.tools.public import Entrance

from SubmarketMerge.tasks import *
from SubmarketMerge.component.tasksObj import *


class Manager(object):
    def __init__(self, pcid, cid, datamonth, cidname):
        Entrance(pcid=pcid, cid=cid, datamonth=datamonth, cidname=cidname)

    @staticmethod
    def run():
        tasks = Tasks()
        tasks.assign(InitCommand(InitFilesMethod))
        tasks.assign(CutCommand(CutWithoutBrandMethod))
        tasks.assign(MergeCommand(IntersectionMethod))
        tasks.assign(EraseCommand(EraseSpecialMethod))
        tasks.assign(EraseCommand(EraseCidnameSimMethod))
        tasks.assign(EraseCommand(EraseCounryMethod))
        tasks.assign(EraseCommand(EraseUselessMethod))
        tasks.assign(EraseCommand(EraseBrandMethod))
        tasks.assign(PairCommand(PairWholeSemanticsMethod))
        tasks.assign(PairCommand(PairLiteralContainMethod))
        tasks.assign(PairCommand(PairEditDistanceMethod))
        tasks.assign(MergeCommand(UnionMethod))
        tasks.assign(EraseCommand(EraseSpecialMethod))
        tasks.assign(EraseCommand(EraseCidnameSimMethod))
        tasks.assign(EraseCommand(EraseCounryMethod))
        tasks.assign(EraseCommand(EraseUselessMethod))
        tasks.assign(EraseCommand(EraseBrandMethod))
        tasks.assign(PairCommand(PairWholeSemanticsMethod))
        tasks.assign(PairCommand(PairLiteralContainMethod))
        tasks.assign(PairCommand(PairEditDistanceMethod, Parameters.pairUnionEditDistanceThreshold))
        tasks.assign(AppendCommand(AppendSpecialMethod))
        tasks.assign(AppendCommand(AppendCountryMethod))
        tasks.assign(StatisticCommand(StatisticAllSubmarketMethod))
        tasks.assign(StatisticCommand(StatisticSubmarketBrandBizMethod))
        tasks.assign(StatisticCommand(StatisticSubmarketBrandSoldMethod))
        tasks.assign(BuildInfoCommand(BuildMainAndTopBrandMethod))
        # tasks.assign(TransCommand(PairTransToSetMethod))
        # tasks.assign(ShowCommand(ShowMethod))
        # tasks.assign(ShowCommand(ShowPairWordsMethod))
        # tasks.assign(ShowCommand(ShowSetWordsMethod))
        # tasks.assign(ShowCommand(ShowTopWordsMethod))
        # tasks.assign(ShowCommand(ShowTopWordsExceptKeepWordsMethod))
        tasks.assign(ClearFileCommand(RemainFinalResultMethod))

        tasks.execute()


if __name__ == '__main__':
    pcid = "2"
    cid = "50008881"
    datamonth = "201810"
    cidname = "phone"

    obj = Manager(pcid=pcid, cid=cid, datamonth=datamonth, cidname=cidname)
    obj.run()

    # show("smDrop")
    # show("smMapping")
