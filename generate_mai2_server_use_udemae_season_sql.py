#coding=utf8
import os
import sys
import xml.etree.ElementTree as ET
import sqlparse
import datetime
from pypika import Table, Query


def parse_ymd(s):
    return datetime.datetime(int("20"+s[:2]), int(s[2:4]), int(s[4:]), 7, 0, 0, 0)

path = sys.argv[1]
sql_list = []

if path != None and path != "":
    table = Table("mai2_game_event")

    g = os.walk(path)

    outputFile = path + "\\udemae_season_opening_time.sql"
    print(path)
    print(outputFile)
    if os.path.exists(outputFile):
        os.remove(outputFile)

    for path, dir_list, file_list in g:  
        for file_name in file_list:  
            if file_name == "UdemaeSeasonEvent.xml":
                filepath = os.path.join(path, file_name)
                tree = ET.parse(filepath)
                root = tree.getroot()
                open_event_id = root.find("openEventId").find("id").text
                startDate = parse_ymd(open_event_id[:6])
                result_event_id = root.find("resultEventId").find("id").text
                endDate = parse_ymd(result_event_id[:6])
                sql_start = (Query.update(table)
                             .set(table.start_date, startDate.strftime("%Y-%m-%d %H:%M:%S.0"))
                             .set(table.end_date, endDate.strftime("%Y-%m-%d %H:%M:%S.0"))
                             .where(table.eventId == int(open_event_id)))
                sql_end = (Query.update(table)
                           .set(table.start_date, endDate.strftime("%Y-%m-%d %H:%M:%S.0"))
                           .set(table.end_date, (endDate + datetime.timedelta(days = 30)).strftime("%Y-%m-%d %H:%M:%S.0"))
                           .where(table.eventId == int(result_event_id)))
                sql_list.append(sqlparse.format(sql_start.get_sql(quote_char="`")))
                sql_list.append(sqlparse.format(sql_end.get_sql(quote_char="`")))

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        for sql in sql_list:
            f.write("".join(sql) + ";\n")