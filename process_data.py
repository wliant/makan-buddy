import csv
import os
import json
from feature_vector import create_image_vector_save_to_file

imageDir = "data/images"
npzDir = "npz"
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
            json.dump(obj, jsonfile, sort_keys=True, indent=4)
    except Exception as e:
        print("error while writing json")
        print(e)

def processImages(part1, part2):
    imageDirectory = os.path.join(imageDir, part1, "{}_{}".format(part1,part2))
    result = {}
    counter=0
    for imgFileName in os.listdir(imageDirectory):
        imageFullPath = os.path.join(imageDirectory, imgFileName)
        print(imageFullPath)
        counter += 1
        outpath = os.path.join(npzDir, "{}_{}_{}.npz".format(part1, part2, counter))
        create_image_vector_save_to_file(imageFullPath, outpath)
        result[imageFullPath.replace("\\", "/")] = outpath.replace("\\", "/")
    return result

errors = []
for f in os.listdir("data"):
    if f.endswith(".csv"):
        part1 = f.split("_")[0]
        print("processing file: {}".format(f))
        with open(os.path.join("data", f), 'r', encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile)
            for row in spamreader:
                try:
                    print(row["Name"])
                    part2 = row["ID"]
                    jsonFile = "json/{}_{}.json".format(part1, part2)
                    jsonData = {col: row[col] for col in columns}
                    jsonData["images"] = processImages(part1, part2)
                    writeJson(jsonFile, jsonData)
                except Exception as e:
                    print("error {}".format(e))
                    jsonData = {col: row[col] for col in columns}
                    errors.append({"data": jsonData, "error": str(e)})

writeJson("process_data_error.json", errors)
                    