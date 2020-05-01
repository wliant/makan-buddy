import json
import os
import random
from MQKNN import MQKNN

nn_file = "nearest_neighbors.json"
restaurant_json_directory = "json"
d = 1792
K = 20
random.seed()
class Intel:
    def __init__(self):
        self.queries = []
        self.restaurants = self.load_restaurants()
        print("number of restaurants: {}", len(self.restaurants))
        #self.neighbors = self.load_neighbors()
        self.queries = []
    def load_restaurants(self):
        results = {}
        for f in os.listdir(restaurant_json_directory):
            if f.endswith(".json"):
                filePath = os.path.join(restaurant_json_directory, f)
                with open(filePath, 'r', encoding="utf-8") as infile:
                    res = json.load(infile)
                    images = list(res["images"].keys())
                    if len(images) > 0:
                        results[f.replace(".json", "")] = res

        return results

    def load_neighbors(self):
        results = {}
        with open(nn_file, 'r', encoding="utf-8") as infile:
            obj = json.load(infile)
            for result in obj:
                results[result["filename"]] = result["similar"]
        return results

    # return image id, image path
    def get_query(self):
        rand_res = random.choice(list(self.restaurants.items()))
        rand_image = random.choice(list(rand_res[1]["images"].items()))

        self.queries.append({"npz": rand_image[1], "path": rand_image[0], "positive": 0, "neutral": 0, "negative": 0})
        return len(self.queries), rand_image[0]

    def update_response(self, image_id, positive, neutral, negative):
        self.queries[image_id-1]["positive"] = positive
        self.queries[image_id-1]["neutral"] = neutral
        self.queries[image_id-1]["negative"] = negative

    def get_result(self):
        neighbors = self.load_neighbors()
        occurrence = {}
        data_files = set()
        query_files = []
        weights = []
        for query in self.queries:
            weights.append(query["positive"] / float(query["positive"] + query["neutral"] + query["negative"]))
            query_files.append(query["npz"])
            nn = neighbors[query["npz"]]
            for i in nn:
                data_files.add(i["filename"])

        mqknn = MQKNN(d, K, data_files, query_files, weights)
        result = mqknn.get_result()

        results = []
        for r in result:
            restaurant_id = self.get_npz_restaurant(r)
            restaurant_obj = self.restaurants[restaurant_id]
            results.append((restaurant_obj["Name"], [i for i in restaurant_obj["images"].keys()]))

        return results[0]
    def get_npz_restaurant(self, npz):
        st = npz.replace("npz/", "").replace(".npz", "")
        split = st.split("_")
        restaurant_id = "{}_{}".format(split[0], split[1])
        return restaurant_id
        #return self.restaurants[restaurant_id]


        

#i = Intel()
#print("init complete")
#for j in range(0, 5):
    #print(i.get_query())
#    id,path = i.get_query()
#    i.update_response(id, 3, 0, 0)

#print("getting result")
#print(i.get_result())