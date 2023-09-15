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
    10,
    22091511,
    22091512,
    22091513,
    22091514,
    22091515,
    22091516,
    22091518,
    22092211,
    22092212,
    22100711,
    22102111,
    22110411,
    22110412,
    22111011,
    22111811,
    22120211,
    22120212,
    22121611,
    22122311,
    22122312,
    23010611,
    23010612,
    23012011,
    23020311,
    23021711,
    23021712,
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
    23040111,
    23041411,
    23042811,
    23051211,
    23052611,
    23052612,
    23060811,
    23062311,
    23063011,
    23070711,
    23070712,
    23072111,
    23080411,
    23081811,
    23081812,
    23090111,
    23091411,
    22091561,
    23032361,
    23032362,
    23071161,
    23081861,
    23091461,
    23091462,
    24021661,
    22100712,
    22100722,
    22100791,
    22102891,
    22120213,
    22120224,
    22120291,
    22122391,
    23020312,
    23020323,
    23020391,
    23022391,
    23042812,
    23042822,
    23042891,
    23051991,
    23060812,
    23060822,
    23060891,
    23063091,
    23072112,
    23072122,
    23072191,
    23081891
]

path = sys.argv[1]
if path != None and path != "":
    table = Table("any_db_you_want")
    sql = Query.into(table).columns("event_id", "start_date", "end_date", "type", "remarks")

    g = os.walk(path)

    outputFile = path + "\open_event_list.sql"
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
                sql = sql.insert(int(event_id), startDate.strftime("%Y-%m-%d %H:%M:%S.0"), "2029-01-01 23:59:59.0", int(infoType), remark)

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        f.write(sqlparse.format(sql.get_sql(quote_char="`")))