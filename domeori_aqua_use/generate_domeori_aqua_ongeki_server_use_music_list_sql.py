#coding=utf8
import os
import sys
import xml.etree.ElementTree as ET
import sqlparse
from pypika import Table, Query


path = sys.argv[1]
if path != None and path != "":
    table = Table("ongeki_game_music")
    sql = Query.into(table).columns("id", "name", "sort_name", "artist_name", "genre", "boss_card_id", "boss_level", "level0", "level1", "level2", "level3", "level4")
    g = os.walk(path)

    outputFile = path + "\ongeki_music_list_domeri_aqua.sql"
    print(path)
    print(outputFile)
    if os.path.exists(outputFile):
        os.remove(outputFile)

    for path, dir_list, file_list in g:  
        for file_name in file_list:  
            if file_name == "Music.xml":
                filepath = os.path.join(path, file_name)
                tree = ET.parse(filepath)
                root = tree.getroot()
                music_id = int(root.find("Name").find("id").text)
                name = root.find("Name").find("str").text
                sort_name = root.find("NameForSort").text
                artist_name = root.find("ArtistName").find("str").text
                genre = root.find("Genre").find("str").text
                boss_card_id = int(root.find("BossCard").find("id").text)
                boss_level = int(root.find("BossLevel").text)
                fumen_list = root.find("FumenData").findall("FumenData")

                sql = sql.insert(music_id)

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        f.write(sqlparse.format(sql.get_sql(quote_char="`")))