import json
import os
import random
from MQKNN import MQKNN

nn_file = "nearest_neighbors.json"
restaurant_json_directory = "json"
d = 1792
K = 30
random.seed()
class Intel:
    def __init__(self):
        self.queries = []
        self.restaurants = self.load_restaurants()
        print("number of restaurants: {}", len(self.restaurants))
        #self.neighbors = self.load_neighbors()
        self.queries = self.load_queries()

    def load_queries(self):
        if os.path.isfile("queries.json"):
            with open("queries.json", "r") as infile:
                result = json.load(infile)
            return result
        else:
            return []
    def write_queries(self):
        with open("queries.json", 'w') as outfile:
            json.dump(self.queries, outfile)

    def load_results(self):
        if os.path.isfile("results.json"):
            with open("results.json", 'r') as infile:
                result = json.load(infile)
            return result
        else:
            return []
    def write_results(self, results):
        with open("results.json", "w") as outfile:
            json.dump(results, outfile)
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
        self.write_queries()
        return len(self.queries), rand_image[0], rand_res[1]["Name"]

    def update_response(self, image_id, positive, neutral, negative):
        self.queries[image_id-1]["positive"] = positive
        self.queries[image_id-1]["neutral"] = neutral
        self.queries[image_id-1]["negative"] = negative
        self.write_queries()


    def calculate_result(self):
        neighbors = self.load_neighbors()
        occurrence = {}
        data_files = set()
        query_files = []
        weights = []
        for query in self.queries:
            w = query["positive"] / float(5)
            if w == 0:
                continue
            weights.append(w)
            query_files.append(query["npz"])
            nn = neighbors[query["npz"]]
            for i in nn:
                data_files.add(i["filename"])

        mqknn = MQKNN(d, K, data_files, query_files, weights)
        result = mqknn.get_result()

        loaded_results = []
        for r in result:
            restaurant_id = self.get_npz_restaurant(r)
            restaurant_obj = self.restaurants[restaurant_id]
            loaded_results.append({"name": restaurant_obj["Name"], "images":[i for i in restaurant_obj["images"].keys()]})
        self.queries = []
        self.write_queries()
        self.write_results(loaded_results)
        print("calculation complete")

    def load_valid_restaurants(self):
        with open("valid_restaurants.json", "r", encoding="utf-8") as jsonfile:
            result = json.load(jsonfile)
        return result
    def get_result(self):
        loaded_results = self.load_results()
        if len(loaded_results) == 0:
            return None
        else:
            returned_result = loaded_results[0]
            name = returned_result["name"]
            images = returned_result["images"]
            valid_restaurants = self.load_valid_restaurants()
            loaded_results = loaded_results[1:]
            while name not in valid_restaurants:
                if len(loaded_results) == 0:
                    self.write_results(loaded_results)
                    return None
                returned_result = loaded_results[0]
                name = returned_result["name"]
                images = returned_result["images"]
                valid_restaurants = self.load_valid_restaurants()
                loaded_results = loaded_results[1:]

            
            self.write_results(loaded_results)
            return (name, images)

    def restart_query(self):
        self.queries = []
        self.write_queries()
    def has_result(self):
        loaded_results = self.load_results()
        return len(loaded_results) > 0
    def get_query_size(self):
        return len(self.queries)
    def get_npz_restaurant(self, npz):
        st = npz.replace("npz/", "").replace(".npz", "")
        split = st.split("_")
        restaurant_id = "{}_{}".format(split[0], split[1])
        return restaurant_id

