# -*- coding:utf-8 -*-


from SubmarketMerge.settings import Parameters, Mode
from SubmarketMerge.tools.utils import load, dump, read


class StatisticMethod(object):
    def __init__(self):
        """Init"""

    def statistic(self):
        """Statistic Function"""
        raise NotImplementedError


class StatisticAllSubmarketMethod(StatisticMethod):
    """Statistic All Submarket Words"""
    def statistic(self):
        if Mode.statsLOCAL:
            try:
                load("statsAllSubItemidSet")
                load("statsAllSubBrandSet")
                load("statsAllSubSellerSet")
                load("statsAllSubBiz30day")
                load("statsAllSubTotalSoldPrice")
                load("statsAllSubSoldAverPrice")

                load("statsAllSubMacroCondition")
                load("statsAllItemidMapping")

                load("statsAllSubBiz30dayShare")
                load("statsAllSubBiz30dayRank")
                load("statsAllSubBiz30dayReRank")
                load("statsAllSubTotalSoldPriceShare")
                load("statsAllSubTotalSoldPriceRank")
                load("statsAllSubTotalSoldPriceReRank")
            except FileNotFoundError:
                print("StatisticAllSubmarketMethod: Don't Have Local Result Files")
            else:
                return

        words = load("submarketWords")
        items = read("factItem")()

        itemid_set = dict()
        brand_set = dict()
        seller_set = dict()
        biz30day = {word: 0 for word in words}
        total_sold_price = {word: 0 for word in words}

        macro_conditions = dict()
        macro_conditions["biz30day"] = 0
        macro_conditions["total"] = 0

        itemid_mapping = dict()

        for k, v in items.iterrows():
            if k % 100 == 0:
                print("process", k, "/", len(items))
            for word in words:
                if word in v["title"]:
                    itemid_set.setdefault(word, set()).add(v["itemid"])
                    if v["brand"] == v["brand"]:
                        brand_set.setdefault(word, set()).add(v["brand"])
                    if v["sellernick"] == v["sellernick"]:
                        seller_set.setdefault(word, set()).add(v["sellernick"])
                    biz30day[word] += v["biz30day"]
                    total_sold_price[word] += v["total_sold_price"]

            macro_conditions.setdefault("itemid", set()).add(v["itemid"])
            if v["brand"] == v["brand"]:
                macro_conditions.setdefault("brand", set()).add(v["brand"])
            if v["sellernick"] == v["sellernick"]:
                macro_conditions.setdefault("seller", set()).add(v["sellernick"])
            macro_conditions["biz30day"] += v["biz30day"]
            macro_conditions["total"] += v["total_sold_price"]

            if v["itemid"] in itemid_mapping.keys():
                print("Warning: Duplicate Itemid", v["itemid"])
            itemid_mapping[v["itemid"]] = (v["brand"], v["biz30day"], v["total_sold_price"])

        sold_price_aver = dict()
        for word in words:
            try:
                sold_price_aver[word] = \
                    round(total_sold_price[word] / biz30day[word], 2)
            except ZeroDivisionError:
                sold_price_aver[word] = 0

        try:
            macro_conditions["aver"] = \
                round(macro_conditions["total"] / macro_conditions["biz30day"], 2)
        except ZeroDivisionError:
            macro_conditions["aver"] = 0

        # itemid_set["macro conditions"] = macro_conditions["itemid"]
        # brand_set["macro conditions"] = macro_conditions["brand"]
        # seller_set["macro conditions"] = macro_conditions["seller"]
        # biz30day["macro conditions"] = macro_conditions["biz30day"]
        # total_sold_price["macro conditions"] = macro_conditions["total"]
        # sold_price_aver["macro conditions"] = macro_conditions["aver"]

        dump(itemid_set, "statsAllSubItemidSet")
        dump(brand_set, "statsAllSubBrandSet")
        dump(seller_set, "statsAllSubSellerSet")
        dump(biz30day, "statsAllSubBiz30day")
        dump(total_sold_price, "statsAllSubTotalSoldPrice")
        dump(sold_price_aver, "statsAllSubSoldAverPrice")

        dump(macro_conditions, "statsAllSubMacroCondition")
        dump(itemid_mapping, "statsAllItemidMapping")

        biz30day_share = dict()
        biz30day_rank = dict()
        biz30day_rerank = dict()
        total_sold_price_share = dict()
        total_sold_price_rank = dict()
        total_sold_price_rerank = dict()

        items = sorted(biz30day.items(), key=lambda x: x[1], reverse=True)
        prev, rank = 0, 0
        for key, value in items:
            try:
                biz30day_share[key] = value / macro_conditions["biz30day"]
            except ZeroDivisionError:
                biz30day_share[key] = 0
            if prev != value:
                rank += 1
                prev = value
            biz30day_rank[key] = rank
            biz30day_rerank.setdefault(rank, list()).append(key)

        items = sorted(total_sold_price.items(), key=lambda x: x[1], reverse=True)
        prev, rank = 0, 0
        for key, value in items:
            try:
                total_sold_price_share[key] = value / macro_conditions["total"]
            except ZeroDivisionError:
                total_sold_price_share[key] = 0
            if prev != value:
                rank += 1
                prev = value
            total_sold_price_rank[key] = rank
            total_sold_price_rerank.setdefault(rank, list()).append(key)

        dump(biz30day_share, "statsAllSubBiz30dayShare")
        dump(biz30day_rank, "statsAllSubBiz30dayRank")
        dump(biz30day_rerank, "statsAllSubBiz30dayReRank")
        dump(total_sold_price_share, "statsAllSubTotalSoldPriceShare")
        dump(total_sold_price_rank, "statsAllSubTotalSoldPriceRank")
        dump(total_sold_price_rerank, "statsAllSubTotalSoldPriceReRank")


class StatisticSubmarketBrandBizMethod(StatisticMethod):
    """Statistic Main Biz30day Submarket Words"""
    def statistic(self, threshold=Parameters.mainBizThreshold):
        if Mode.statsLOCAL:
            try:
                load("statsSubBrandBizNum")
                load("statsSubBrandBizShare")
                load("statsSubBrandBizRank")
                load("statsSubBrandBizReRank")
            except FileNotFoundError:
                print("StatisticSubmarketBrandBizMethod: Don't Have Local Result Files")
            else:
                return

        words = load("submarketWords")
        submarket_biz30day = load("statsAllSubBiz30day")
        itemid_set = load("statsAllSubItemidSet")
        itemid_mapping = load("statsAllItemidMapping")

        submarket_brand_num = {word: dict() for word in words}
        submarket_brand_share = {word: dict() for word in words}
        submarket_brand_rank = {word: dict() for word in words}
        submarket_brand_rerank = {word: dict() for word in words}

        for word in words:
            try:
                itemids = itemid_set[word]
            except KeyError:
                continue
            for itemid in itemids:
                brand, biz30day, _ = itemid_mapping[itemid]
                if brand != brand or not brand:
                    continue
                if brand in submarket_brand_num[word].keys():
                    submarket_brand_num[word][brand] += biz30day
                else:
                    submarket_brand_num[word][brand] = biz30day

            items = sorted(submarket_brand_num[word].items(), key=lambda x: x[1], reverse=True)
            prev, rank = 0, 0
            for brand, value in items:
                try:
                    submarket_brand_share[word][brand] = value / submarket_biz30day[word]
                except ZeroDivisionError:
                    submarket_brand_share[word][brand] = 0
                if prev != value:
                    rank += 1
                    prev = value
                submarket_brand_rank[word][brand] = rank
                submarket_brand_rerank[word].setdefault(rank, list()).append(brand)
                submarket_brand_rerank[word][rank].sort()

        dump(submarket_brand_num, "statsSubBrandBizNum")
        dump(submarket_brand_share, "statsSubBrandBizShare")
        dump(submarket_brand_rank, "statsSubBrandBizRank")
        dump(submarket_brand_rerank, "statsSubBrandBizReRank")


class StatisticSubmarketBrandSoldMethod(StatisticMethod):
    """Statistic Main Total Sold Price Submarket Words"""
    def statistic(self, threshold=Parameters.mainSoldThreshold):
        if Mode.statsLOCAL:
            try:
                load("statsSubBrandSoldNum")
                load("statsSubBrandSoldShare")
                load("statsSubBrandSoldRank")
                load("statsSubBrandSoldReRank")
            except FileNotFoundError:
                print("StatisticSubmarketBrandSoldMethod: Don't Have Local Result Files")
            else:
                return

        words = load("submarketWords")
        submarket_total_sold_price = load("statsAllSubTotalSoldPrice")
        itemid_set = load("statsAllSubItemidSet")
        itemid_mapping = load("statsAllItemidMapping")

        submarket_brand_num = {word: dict() for word in words}
        submarket_brand_share = {word: dict() for word in words}
        submarket_brand_rank = {word: dict() for word in words}
        submarket_brand_rerank = {word: dict() for word in words}

        for word in words:
            try:
                itemids = itemid_set[word]
            except KeyError:
                continue
            for itemid in itemids:
                brand, _, total_sold_price = itemid_mapping[itemid]
                if brand != brand or not brand:
                    continue
                if brand in submarket_brand_num[word].keys():
                    submarket_brand_num[word][brand] += total_sold_price
                else:
                    submarket_brand_num[word][brand] = total_sold_price

            items = sorted(submarket_brand_num[word].items(), key=lambda x: x[1], reverse=True)
            prev, rank = 0, 0
            for brand, value in items:
                try:
                    submarket_brand_share[word][brand] = value / submarket_total_sold_price[word]
                except ZeroDivisionError:
                    submarket_brand_share[word][brand] = 0
                if prev != value:
                    rank += 1
                    prev = value
                submarket_brand_rank[word][brand] = rank
                submarket_brand_rerank[word].setdefault(rank, list()).append(brand)
                submarket_brand_rerank[word][rank].sort()

        dump(submarket_brand_num, "statsSubBrandSoldNum")
        dump(submarket_brand_share, "statsSubBrandSoldShare")
        dump(submarket_brand_rank, "statsSubBrandSoldRank")
        dump(submarket_brand_rerank, "statsSubBrandSoldReRank")


class UseLocalStatsMethod(StatisticMethod):
    """Use Local Files As The Result Of Statistic Method"""
    def __init__(self, method):
        self.method = method

    def statistic(self):
        pass
