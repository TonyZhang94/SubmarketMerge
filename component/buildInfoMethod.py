# -*- coding:utf-8 -*-


from SubmarketMerge.settings import Parameters, FileBase
from SubmarketMerge.tools.public import Entrance
from SubmarketMerge.tools.utils import load, dump, read


class BuildInfoMethod(object):
    def __init__(self):
        """Init"""

    def build(self):
        """Build Function"""
        raise NotImplementedError

    @staticmethod
    def dump(data, name):
        pcid, cid, _ = Entrance().params
        dump(data, _, repath=FileBase.result.format(pcid=pcid, cid=cid, name=name))


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
        # biz_brand_rank = load("statsSubBrandBizRank")
        biz_brand_rerank = load("statsSubBrandBizReRank")

        sold_brand_num = load("statsSubBrandSoldNum")
        sold_brand_share = load("statsSubBrandSoldShare")
        # sold_brand_rank = load("statsSubBrandSoldRank")
        sold_brand_rerank = load("statsSubBrandSoldReRank")

        for word in words:
            info[word] = dict()
            if word not in itemid_set.keys():
                info[word]["inTitle"] = False
                continue
            info[word]["inTitle"] = True

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

            biz_word_brand_num = 0
            for rank, brands in biz_brand_rerank[word].items():
                biz_word_brand_num += len(brands)
            biz_main_size = biz_word_brand_num * self.threshold["biz main"]
            if biz_main_size < self.threshold["biz top"]:
                biz_main_size = self.threshold["biz top"]

            rank, num = 0, 0
            info[word]["top biz brand"] = dict()
            while True:
                rank += 1
                try:
                    brands = biz_brand_rerank[word][rank]
                except KeyError:
                    # print("Don't have enough words as expect.")
                    break
                if num < biz_main_size:
                    info[word].setdefault("main biz brand", list()).extend(brands)

                if num < self.threshold["biz top"]:
                    for brand in brands:
                        info[word]["top biz brand"][brand] = dict()
                        info[word]["top biz brand"][brand]["num"] = biz_brand_num[word][brand]
                        info[word]["top biz brand"][brand]["share"] = biz_brand_share[word][brand]
                        info[word]["top biz brand"][brand]["rank"] = rank

                num += len(brands)
                if biz_main_size <= num and self.threshold["biz top"] <= num:
                    break

            sold_word_brand_num = 0
            for rank, brands in sold_brand_rerank[word].items():
                sold_word_brand_num += len(brands)
            sold_main_size = sold_word_brand_num * self.threshold["sold main"]
            if sold_main_size < self.threshold["sold top"]:
                sold_main_size = self.threshold["sold top"]

            rank, num = 0, 0
            info[word]["top sold brand"] = dict()
            while True:
                rank += 1
                try:
                    brands = sold_brand_rerank[word][rank]
                except KeyError:
                    # print("Don't have enough words as expect.")
                    break
                if num < sold_main_size:
                    info[word].setdefault("main sold brand", list()).extend(brands)

                if num < self.threshold["sold top"]:
                    for brand in brands:
                        info[word]["top sold brand"][brand] = dict()
                        info[word]["top sold brand"][brand]["num"] = sold_brand_num[word][brand]
                        info[word]["top sold brand"][brand]["share"] = sold_brand_share[word][brand]
                        info[word]["top sold brand"][brand]["rank"] = rank

                num += len(brands)
                if sold_main_size <= num and self.threshold["sold top"] <= num:
                    break

        super().dump(info, "submarketInfo")


class BuildTopBizBrandsMethod(BuildInfoMethod):
    """Statistic Top Biz30day Brands"""
    def build(self):
        items = read("factItem")()
        items = items[items["brand"] == items["brand"]]
        macro_condition = load("statsAllSubMacroCondition")

        def sum_biz(df):
            biz_sum = df["biz30day"].sum()
            df["biz_sum"] = biz_sum
            try:
                df["biz_share"] = biz_sum / macro_condition["biz30day"]
            except ZeroDivisionError:
                df["biz_share"] = 0
            return df

        items["biz30day"] = items["biz30day"].fillna(0)
        items = items.groupby(["brand"]).apply(sum_biz).drop_duplicates(["brand"]).sort_values(
            "biz_sum", ascending=False)
        items = items[["brand", "biz_sum", "biz_share"]]

        prev, rank = 0, 0
        for k, v in items.iterrows():
            if prev != v["biz_sum"]:
                rank += 1
                prev = v["biz_sum"]
            items.at[k, "rank"] = rank

        super().dump(items, "statsTopBizBrands")


class BuildTopSoldBrandsMethod(BuildInfoMethod):
    """Statistic Top Total Sold Price Brands"""
    def build(self):
        items = read("factItem")()
        items = items[items["brand"] == items["brand"]]
        macro_condition = load("statsAllSubMacroCondition")

        def sum_sold(df):
            sold_sum = df["total_sold_price"].sum()
            df["sold_sum"] = sold_sum
            try:
                df["sold_share"] = sold_sum / macro_condition["total"]
            except ZeroDivisionError:
                df["sold_share"] = 0
            return df

        items["total_sold_price"] = items["total_sold_price"].fillna(0)
        items = items.groupby(["brand"]).apply(sum_sold).drop_duplicates(["brand"]).sort_values(
            "sold_sum", ascending=False)
        items = items[["brand", "sold_sum", "sold_share"]]

        prev, rank = 0, 0
        for k, v in items.iterrows():
            if prev != v["sold_sum"]:
                rank += 1
                prev = v["sold_sum"]
            items.at[k, "rank"] = rank

        super().dump(items, "statsTopSoldBrands")
