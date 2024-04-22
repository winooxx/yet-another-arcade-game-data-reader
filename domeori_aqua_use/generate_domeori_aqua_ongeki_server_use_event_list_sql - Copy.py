#coding=utf8
import os
import sys
import xml.etree.ElementTree as ET
import sqlparse
from pypika import Table, Query


path = sys.argv[1]
if path != None and path != "":
    table = Table("ongeki_game_event")
    sql = Query.into(table).columns("id")

    g = os.walk(path)

    outputFile = path + "\ongeki_open_event_list_domeri_aqua.sql"
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
                event_id = root.find("Name").find("id").text
                sql = sql.insert(int(event_id))

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        f.write(sqlparse.format(sql.get_sql(quote_char="`")))