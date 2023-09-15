#coding=utf8
import os
import xml.etree.ElementTree as ET
import csv
import math
import sys

path = sys.argv[1]
if path != None and path != "":
    g = os.walk(path)

    outputFile = path + "\score_level_sorted.csv"
    print(path)
    print(outputFile)
    if os.path.exists(outputFile):
        os.remove(outputFile)

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        writer = csv.writer(f)
        # writer.writerow("歌曲ID, 歌曲名, 基本BASIC, 进阶ADVANCED, 专家EXPERT, 大师MASTER, MASTER鸟+Rating, 宗师Re:MASTER, Re:MASTER鸟+Rating".split(","))
        writer.writerow("歌曲ID, 歌曲名, 大师MASTER, MASTER鸟+Rating, 宗师Re:MASTER, Re:MASTER鸟+Rating".split(","))
        for path, dir_list, file_list in g:  
            for file_name in file_list:  
                if file_name == "Music.xml":
                    filepath = os.path.join(path, file_name)
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    notes = root.find("notesData").findall("Notes")
                    # get all data
                    id = root.find("name").find("id").text
                    name = root.find('name').find('str').text
                    # basic = notes[0].find("level").text + "." + notes[0].find("levelDecimal").text
                    # advanced = notes[1].find("level").text + "." + notes[1].find("levelDecimal").text
                    # expert = notes[2].find("level").text + "." + notes[2].find("levelDecimal").text
                    master = notes[3].find("level").text + "." + notes[3].find("levelDecimal").text
                    masterRating = float(master) * 14
                    remaster = notes[4].find("level").text + "." + notes[4].find("levelDecimal").text
                    remasterRating = float(remaster) * 14
                    if float(remaster) != 0.0:
                        writer.writerow([id, name, master, math.ceil(masterRating), remaster, math.ceil(remasterRating)])
                    else:
                        writer.writerow([id, name, master, math.ceil(masterRating)])
                    
