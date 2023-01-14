import csv
import json
import os

dir_path = f"{os.getcwd()}/result"

json_list = []

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.json' in file:
            file_path = os.path.join(root, file)
            json_list.append(file_path)

file1 = json_list[0]
file2 = json_list[1]

with open(file1) as file_1:
    data1 = json.load(file_1)

with open(file2) as file_2:
    data2 = json.load(file_2)

with open("mergedfile.json", "w", encoding="utf-8") as new_file:
    json.dump(data1+data2, new_file, indent='\t', ensure_ascii=False)
