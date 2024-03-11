#coding=utf8
import os
import sys
import xml.etree.ElementTree as ET
import sqlparse
from pypika import Table, Query


path = sys.argv[1]
if path != None and path != "":
    table = Table("ongeki_game_event")
    sql = Query.into(table).columns("name", "type", "enable", "start_date", "end_date","remarks", "version", "event_id")

    g = os.walk(path)

    outputFile = path + "\ongeki_open_event_list.sql"
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
                dataName = root.find("dataName").text
                event_id = root.find("Name").find("id").text
                remark = root.find("Name").find("str").text
                version = int(event_id[0:3])
                enable = 1 if version < 145 else 0
                sql = sql.insert(dataName, 0, enable, "2024-03-07 07:00:00.0", "2029-01-01 23:59:59.0", remark, version, int(event_id))

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        f.write(sqlparse.format(sql.get_sql(quote_char="`")))