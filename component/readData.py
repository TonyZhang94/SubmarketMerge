# -*- coding:utf-8 -*-

from SubmarketMerge.tools.engine import Engine
from SubmarketMerge.tools.public import Entrance
from SubmarketMerge.tools.decorator import *
from SubmarketMerge.settings import *


def read_data(src, fname, sql, db):
    try:
        if not src:
            raise ReadDBException
        df = pd.read_csv(fname, encoding="utf-8", index_col=0)
    except (FileExistsError, FileNotFoundError, ReadDBException) as flag:
        print(sql)
        engine = Engine()
        try:
            df = pd.read_sql_query(sql, engine(db))
        except Exception as e:
            raise e
        else:
            if flag.__doc__ != "Choose Get Data From DB":
                df.to_csv(fname, encoding="utf-8")
    except Exception as e:
        raise e
    return df


@logging
def get_sdSubmarket_info(src=Mode.srcLOCAL):
    pcid, cid, _ = Entrance().params
    fname = FileBase.info.format(name="sdSubmarket", pcid=pcid, cid=cid)
    fields = ["*"]
    field, table = ", ".join(fields), "sd_submarket.pcid{pcid}".format(pcid=pcid)
    sql = "SELECT {field} FROM {table} WHERE cid='{cid}';".format(
        field=field, table=table, cid=cid)
    return read_data(src, fname=fname, sql=sql, db="standard_library")


# @logging
# def get_hotWords_info(src=Mode.srcLOCAL):
#     pcid, cid, _ = Entrance().params
#     fname = FileBase.info.format(name="hotWords", pcid=pcid, cid=cid)
#     fields = ["*"]
#     field, table = ", ".join(fields), "charts.dw_mj_hotwords_submarket"
#     sql = "SELECT {field} FROM {table} WHERE pcid='{pcid}' and cid='{cid}';".format(
#         field=field, table=table, pcid=pcid, cid=cid)
#     return read_data(src, fname=fname, sql=sql, db="report_dg")


@logging
def get_hotWords_info(src=Mode.srcLOCAL):
    pcid, cid, datamonth = Entrance().params
    fname = FileBase.info.format(name="hotWords", pcid=pcid, cid=cid)
    fields = ["*"]
    field, table = ", ".join(fields), "hotwords.mj_hot_words_pcid{pcid}".format(pcid=pcid)
    sql = "SELECT {field} FROM {table} WHERE cid='{cid}' and datamonth~'{datamonth}';".format(
        field=field, table=table, cid=cid, datamonth=datamonth)
    return read_data(src, fname=fname, sql=sql, db="raw_mj_category")


@logging
@ignore_warning
def get_factSubmarket_info(src=Mode.srcLOCAL):
    pcid, cid, datamonth = Entrance().params
    fname = FileBase.info.format(name="factSubmarket", pcid=pcid, cid=cid)
    fields = ["*"]
    field, table = ", ".join(fields), "fact_submarket.pcid{pcid}".format(pcid=pcid)
    sql = "SELECT {field} FROM {table} WHERE cid='{cid}' and datamonth='{datamonth}';".format(
        field=field, table=table, cid=cid, datamonth=datamonth)
    return read_data(src, fname=fname, sql=sql, db="fact_library")


@logging
def get_factItem_info(src=Mode.srcLOCAL):
    pcid, cid, datamonth = Entrance().params
    fname = FileBase.info.format(name="factItem", pcid=pcid, cid=cid)
    fields = ["*"]
    field, table = ", ".join(fields), "fact_item_pcid{pcid}.cid{cid}".format(pcid=pcid, cid=cid)
    sql = "SELECT {field} FROM {table} WHERE datamonth='{datamonth}';".format(
        field=field, table=table, datamonth=datamonth)
    return read_data(src, fname=fname, sql=sql, db="fact_library")
