#coding=utf8
import os
import sys
import xml.etree.ElementTree as ET
import sqlparse
from datetime import datetime
from pypika import Table, Query


def parse_ymd(s):
    return datetime(int("20"+s[:2]), int(s[2:4]), int(s[4:]), 7, 0, 0, 0)

exception_event_list = [
    0,
    1,
    10
]

expired_introduction_event_list = [
    22091511,
    22091512,
    22091513,
    22091514,
    22091515,
    22091516,
    22091518,
    22091561,
    22092211,
    22092212,
    22100711,
    22100712,
    22100791,
    22102111,
    22102891,
    22110411,
    22110412,
    22111011,
    22111811,
    22120211,
    22120212,
    22120213,
    22120291,
    22121611,
    22122311,
    22122312,
    22122391,
    23010611,
    23010612,
    23012011,
    23020311,
    23020312,
    23020391,
    23021711,
    23021712,
    23022391,
    23030211,
    23030212,
    23031011,
    23032311,
    23032312,
    23032313,
    23032314,
    23032315,
    23032316,
    23032317,
    23032361,
    23032362,
    23040111,
    23041411,
    23042811,
    23042812,
    23042891,
    23051211,
    23051991,
    23052611,
    23052612,
    23060811,
    23060812,
    23060891,
    23062311,
    23063011,
    23063091,
    23070711,
    23070712,
    23071161,
    23072111,
    23072112,
    23072191,
    23080411,
    23081811,
    23081812,
    23081861,
    23081891,
    23090111,
    23091411,
    23091412,
    23091413,
    23091414,
    23091415,
    23091417,
    23091461,
    23091462,
    23092211,
    23100611,
    23100612,
    23100691,
    23101211,
    23101212,
    23102011,
    23102791,
    23110211,
    23111011,
    23112411,
    23112412,
    23112413,
    23112414,
    23112415,
    23112491,
    23120811,
    23121511,
    23121591,
    23122211,
    23122511,
    24011111,
    24012611,
    24012612,
    24012613,
    24020211,
    24021611,
    24021612,
    24021621,
    24021661,
    24021691,
    24022911,
    24022912,
    24022913,
    24030811,
    24030812,
    24030813,
    24030891,
    240321061,
    240321062
]

path = sys.argv[1]
if path != None and path != "":
    table = Table("mai2_game_event_template")
    sql = Query.into(table).columns("event_id", "start_date", "end_date", "type", "template_id")

    g = os.walk(path)

    outputFile = path + "\open_event_template_list.sql"
    print(path)
    print(outputFile)
    if os.path.exists(outputFile):
        os.remove(outputFile)

    for path, dir_list, file_list in g:  
        for file_name in file_list:  
            if file_name == "Event.xml":
                filepath = os.path.join(path, file_name)
                tree = ET.parse(filepath)
                root = tree.getroot()
                event_id = root.find("name").find("id").text
                if int(event_id) in exception_event_list:
                    continue
                remark = root.find("name").find("str").text
                infoType = root.find('infoType').text
                startDate = parse_ymd(remark[:6])
                if int(event_id) in expired_introduction_event_list:
                    sql = sql.insert(int(event_id), startDate.strftime("%Y-%m-%d %H:%M:%S.0"), "2024-03-21 07:00:01.0", int(infoType), 6)
                else:
                    sql = sql.insert(int(event_id), startDate.strftime("%Y-%m-%d %H:%M:%S.0"), "2029-01-01 23:59:59.0", int(infoType), 6)

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        f.write(sqlparse.format(sql.get_sql(quote_char="`")))