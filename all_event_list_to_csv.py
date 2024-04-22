#coding=utf8
import os
import xml.etree.ElementTree as ET
import csv
from datetime import datetime
import sys

def parse_ymd(s):
    return datetime(int("20"+s[:2]), int(s[2:4]), int(s[4:]), 7, 0, 0, 0)

path = sys.argv[1]
if path != None and path != "":
    g = os.walk(path)

    outputFile = path + "\\all_event_list.csv"
    print(path)
    print(outputFile)
    if os.path.exists(outputFile):
        os.remove(outputFile)

    with open(outputFile, "w", newline='', encoding='utf_8_sig') as f:
        writer = csv.writer(f)
        writer.writerow("event_id, start_date, infoType, remarks".split(","))
        for path, dir_list, file_list in g:  
            for file_name in file_list:  
                if file_name == "Event.xml":
                    filepath = os.path.join(path, file_name)
                    tree = ET.parse(filepath)
                    root = tree.getroot()
                    event_id = root.find("name").find("id").text
                    remark = root.find("name").find("str").text
                    infoType = root.find('infoType').text
                    if event_id == "0" or event_id == "1" or event_id == "10":
                        writer.writerow([event_id, "常时", infoType, remark])
                    else:
                        startDate = parse_ymd(remark[:6])
                        writer.writerow([event_id, startDate, infoType, remark])
