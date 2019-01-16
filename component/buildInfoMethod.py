# -*- coding:utf-8 -*-


from SubmarketMerge.settings import Parameters
from SubmarketMerge.tools.utils import load, dump, read


class BuildInfoMethod(object):
    def __init__(self):
        """Init"""

    def build(self):
        """Build Function"""


class BuildMainAndTopBrandMethod(BuildInfoMethod):
    """Construct Main Brand Info, Top Brand Info And  Other Info Together"""
    def __init__(self):
        self.threshold = {
            "biz main": Parameters.mainBizThreshold,
            "biz top": Parameters.topBizNum,
            "sold main": Parameters.mainSoldThreshold,
            "sold top": Parameters.topSoldNum
        }

    def build(self):
        words = load("submarketWords")
        info = dict()

        itemid_set = load("statsAllSubItemidSet")
        brand_set = load("statsAllSubBrandSet")
        seller_set = load("statsAllSubSellerSet")
        biz30day = load("statsAllSubBiz30day")
        total_sold_price = load("statsAllSubTotalSoldPrice")
        sold_price_aver = load("statsAllSubSoldAverPrice")

        biz30day_share = load("statsAllSubBiz30dayShare")
        biz30day_rank = load("statsAllSubBiz30dayRank")
        total_sold_price_share = load("statsAllSubTotalSoldPriceShare")
        total_sold_price_rank = load("statsAllSubTotalSoldPriceRank")

        biz_brand_num = load("statsSubBrandBizNum")
        biz_brand_share = load("statsSubBrandBizShare")
        biz_brand_rank = ("statsSubBrandBizRank")
        biz_brand_rerank = load("statsSubBrandBizReRank")
        biz_main_size = len(biz_brand_rerank) * self.threshold["biz main"]

        sold_brand_num = load("statsSubBrandSoldNum")
        sold_brand_share = load("statsSubBrandSoldShare")
        sold_brand_rank = ("statsSubBrandSoldRank")
        sold_brand_rerank = load("statsSubBrandSoldReRank")
        sold_main_size = len(sold_brand_rerank) * self.threshold["sold main"]

        for word in words:
            info[word] = dict()
            if word not in itemid_set.keys():
                print(word, "not in title")
                info[word]["inTitle"] = False
                continue
            info[word]["in title flag"] = True

            info[word]["itemid set"] = itemid_set[word]
            info[word]["brand set"] = brand_set[word]
            info[word]["seller set"] = seller_set[word]
            info[word]["biz30day"] = biz30day[word]
            info[word]["total sold price"] = total_sold_price[word]
            info[word]["sold price aver"] = sold_price_aver[word]

            info[word]["biz30day share"] = biz30day_share[word]
            info[word]["biz30day rank"] = biz30day_rank[word]
            info[word]["total sold price share"] = total_sold_price_share[word]
            info[word]["total sold price rank"] = total_sold_price_rank[word]

            for rank, brands in biz_brand_rerank[word].items():
                if rank < biz_main_size:
                    info[word].setdefault("main biz brand", list()).extend(brands)

                if rank < self.threshold["biz top"]:
                    info[word]["top biz brand"] = dict()
                    for brand in brands:
                        info[word]["top biz brand"][brand] = dict()
                        info[word]["top biz brand"][brand]["num"] = biz_brand_num[word][brand]
                        info[word]["top biz brand"][brand]["share"] = biz_brand_share[word][brand]
                        info[word]["top biz brand"][brand]["rank"] = rank

            for rank, brands in sold_brand_rerank[word].items():
                if rank < sold_main_size:
                    info[word].setdefault("main sold brand", list()).extend(brands)

                if rank < self.threshold["sold top"]:
                    info[word]["top sold brand"] = dict()
                    for brand in brands:
                        info[word]["top sold brand"][brand] = dict()
                        info[word]["top sold brand"][brand]["num"] = sold_brand_num[word][brand]
                        info[word]["top sold brand"][brand]["share"] = sold_brand_share[word][brand]
                        info[word]["top sold brand"][brand]["rank"] = rank

        dump(info, "SubmarketInfo")
