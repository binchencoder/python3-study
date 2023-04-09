#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from collections import namedtuple
import jsonpickle

# res = requests.get(
#     url='http://ws.webxml.com.cn/WebServices/WeatherWS.asmx/getRegionProvince')
# print(res.text)

# get entity types


class BaseResponse:
    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message


class PagerResponse(BaseResponse):
    def __init__(self, total, data, hasNext):
        self.total = total
        self.data = data
        self.hasNext = hasNext


class entityPageItem:
    def __init__(self, geoType, hasChild, name, entityTypeId, parentId):
        self.geoType = geoType
        self.hasChild = hasChild
        self.name = name
        self.entityTypeId = entityTypeId
        self.parentId = parentId

# 重写JSONEncoder的default方法，object转换成dict


# class BaseRespDecode(json.JSONDecoder):
#     def decode(self, s):
#         dic = super().decode(s)
#         return BaseResponse(dic['code'], dic['data'], dic['message'])

def customEntityTypeDecoder(entityDict):
    return namedtuple('X', entityDict.keys())(*entityDict.values())


try:
    jsonRes = requests.post(
        url='https://engine-dev.piesat.cn/bpaas/janus/gateway/api',
        headers={
            "Content-Type": "application/json",
            "x-api": "knowledge.build.getEntityTypePage",
            "x-token": "512eec2b6b797f3abdcd4644d4403f15",
            "x-team-id": "WdWPMWBJUl9UzFPaeS0bK",
            "x-app": "rPvyWAC0cvfT66TH1UbO",
            "x-client": "WEB",
            "x-host-app-id": "engine",
            "x-stage": "PRE",
            "x-gw-version": "2",
            "x-nonce": "fdc91293-3db3-4ea5-9474-27a4864d8227",
            "x-ts": "1651823741657",
        },
        json={
            "ontologyId": "528619154082930688",
            "parentId": "0",
            "name": "",
            "pageNumber": 1,
            "pageSize": 100
        })
except Exception as e:
    print(e)
finally:
    print('finally')

print(jsonRes.text)
print("\n===========")
# Parse JSON into an object with attributes corresponding to dict keys.
pagerResponse = json.loads(jsonRes.text, object_hook=customEntityTypeDecoder)
print(pagerResponse)
print("\n===========")
print(pagerResponse.data.data.pop().name)
