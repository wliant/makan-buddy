import csv
import os
import json

columns =[
    #'', 
    'ID', 'Name', 'URL', 
    'Headlines', 'Reviews', 'Overall Ranking', 
    'Category Ranking', 'Score', 'Area', 'Address', 
    'Locality', 'Country', 'Claim Status', 'Meal Time', 
    'Cuisine', 'Features', 'Tags', 'Opening Days', 
    'Opening Hours', 'Reserve Table', 'Order Online']

def writeJson(filename, obj):
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(obj, jsonfile)
    except Exception as e:
        print("error while writing json")
        print(e)
    
for f in os.listdir("data"):
    if f.endswith(".csv"):
        part1 = f.split("_")[0]
        with open(os.path.join("data", f), 'r', encoding="utf-8") as csvfile:
            try:
                spamreader = csv.DictReader(csvfile)
                for row in spamreader:
                    part2 = row["ID"]
                    jsonFile = "json/{}_{}.json".format(part1, part2)
                    writeJson(jsonFile, {col: row[col] for col in columns})
            except Exception as e:
                print("error while reading csv row {}", row)
                print(e)


