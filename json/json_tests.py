#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# json 字符串
json_string = (
    '[{"Table": "Table S1: Regional usage of antibiotics in China in 2013", "Year": "2013", "City": "China", "Data": {"regions": "East China", "sulfonamides": "2270", "tetracyclines": "3710", "fluoroquinolones": "7290", "macrolides": "14800", "β-lactamsa": "10700", "othersb": "", "totalc": "38800"}},'
    '{"Table": "Table S1: Regional usage of antibiotics in China in 2013", "Year": "2013", "City": "China", "Data": {"regions": "North China", "sulfonamides": "1660", "tetracyclines": "2520", "fluoroquinolones": "6700", "macrolides": "9560", "β-lactamsa": "7410", "othersb": "", "totalc": "27900"}}]'
)


def parseJson():
    json_arr = json.loads(json_string)
    print(json_arr)
    for o in json_arr:
        data = o["Data"]
        if len(data) == 0:
            continue
        for k, v in data.items():
            print(k, v)


if __name__ == "__main__":
    parseJson()
