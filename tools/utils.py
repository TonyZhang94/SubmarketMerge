# -*- coding:utf-8 -*-

import _pickle
import inspect
import os

from SubmarketMerge.tools.public import *
import SubmarketMerge.component.readData
from SubmarketMerge.settings import *


def dump(data, name, force=False, repath=None):
    if Mode.savePKL or force:
        pcid, cid, _ = Entrance().params
        if repath is None:
            repath = FileBase.temporary.format(pcid=pcid, cid=cid, name=name)
        with open(repath, mode="wb") as fp:
            _pickle.dump(data, fp)


def add_dump(data, name, repath=None):
    try:
        _data = load(name, repath)
    except FileNotFoundError:
        _data = set()
    else:
        data = data | _data
    finally:
        dump(data, name, repath)


def load(name, repath=None):
    pcid, cid, _ = Entrance().params
    if repath is None:
        repath = FileBase.temporary.format(pcid=pcid, cid=cid, name=name)
    with open(repath, mode="rb") as fp:
        data = _pickle.load(fp)
    return data


def show(name, repath=None):
    data = load(name, repath)
    print("========= Show %s Size %r =========" % (name, len(data)))
    if isinstance(data, dict):
        for k, v in data.items():
            print(k, v)
    else:
        for v in data:
            print(v)


def show_word(word):
    pcid, cid, _ = Entrance().params
    info = load(_, repath=FileBase.result.format(pcid=pcid, cid=cid, name="submarketInfo"))
    print("========= Show %s =========" % word)
    for k, v in info[word].items():
        if isinstance(v, dict):
            print(k)
            for kk, vv in v.items():
                print(kk, vv)
        else:
            print(k, v)


def read(src):
    funcs = {name: func for name, func in inspect.getmembers(
        SubmarketMerge.component.readData, inspect.isfunction) if "_info" in name}
    try:
        return funcs["get_%s_info" % src]
    except KeyError:
        # print("Read Data Function Key Error:", "get_%s_info" % src)
        pass
    try:
        func = funcs["get_%ss_info" % src]
        # print("Read Data Function Key Is:", "get_%ss_info" % src)
        return func
    except KeyError:
        pass
    try:
        if "s" == src[-1]:
            func = funcs["get_%s_info" % src[: -1]]
            # print("Read Data Function Key Is:", "get_%s_info" % src[: -1])
            return func
    except KeyError:
        pass
    raise RegisterDBException


def make_trantab(src, dst=""):
    trantab = dict()
    for item in src:
        trantab[ord(item)] = dst
    return trantab


def clear_brand(text, co):
    if not isinstance(text, str) \
            or not isinstance(co, str):
        return ""
    if "/" in co:
        try:
            en, zh = co.split("/")
        except ValueError:
            return text
        except Exception as e:
            raise e
        else:
            return text.replace(co, "").replace(en, "").replace(zh, "")
    else:
        return text.replace(co, "")
