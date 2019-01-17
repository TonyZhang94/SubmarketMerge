# -*- coding:utf-8 -*-


def knowledge_useless():
    useless_words = ["新品", "清仓", "降价", "促销", "秒杀", "只限", "购物", "国庆", "五一", "双十一", "双十二",
                     "抢鲜", "抵扣", "特价", "活动", "开业", "全场", "特惠", "包邮", "新款", "打折", "新年",
                     "新春", "迎新", "减价", "新店", "狂欢", "限时", "限购", "全国", "半价", "专属", "活动",
                     "换季", "店庆", "团购", "专享", "淘宝", "天猫", "京东", "爆款", "满减", "一口价", "回馈",
                     "年末", "周年", "同款", "折扣", "其他", "其它", "其他品牌", "淘金币", "双10一", "买", "减",
                     "批发", "快递", "代购", "点券", "疯抢", "薄利多销", "惊喜价", "亏本", "发货", "超值", "现货",
                     "涨价", "冲销量", "已售", "推荐", "出租", "尝鲜价", "冰点价", "甩卖", "酬宾", "清货", "包年",
                     "包月", "即将", "拍前", "节日大促", "晒图", "同款", "旗舰店", "专业", "品牌", "专柜", "专用", "官方"
                     ]
    return useless_words


def knowledge_country():
    country_base = ["中", "日", "韩", "英", "法", "美", "泰"]
    country = list()
    country.extend([x+"国" for x in country_base])
    country.extend([x+"式" for x in country_base])
    country.extend([x+"系" for x in country_base])

    other_country = ["欧式", "意式", "港式", "台湾"]
    country.extend(other_country)

    country_key = set()
    country_map = dict()
    for base in country_base:
        key = base + "式"
        country_key.add(key)
        country_map[key] = set()
        country_map[key].add(key)
        country_map[key].add(base + "系")
        country_map[key].add(base + "国")

    for other in other_country:
        key = other
        country_key.add(key)
        country_map[key] = set()
        country_map[key].add(key)

    country.append("意大利")
    country_map["意式"].add("意大利")
    country.append("欧美")
    country_map["欧式"].add("欧美")
    country.append("香港")
    country_map["港式"].add("香港")
    country.append("日本")
    country_map["日式"].add("日本")

    return set(country), country_key, country_map


def common_char():
    chars = ["色", "款", "式", "防", "无"]
    return set(chars)
