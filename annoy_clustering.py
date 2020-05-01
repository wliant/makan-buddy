import time
import json
from annoy import AnnoyIndex
from scipy import spatial
import glob
import numpy as np

npz_dimension = 1792
n_nearest_neighbors = 200
trees = 10000

allfiles = glob.glob('npz/*.npz')
file_index_to_file_name = {}
file_index_to_file_vector = {}
start_time = time.time()

t = AnnoyIndex(npz_dimension, metric='angular')
print("--------------------------------------------")
print("Step.1 - ANNOY index generation - Started at %s" %time.ctime())
print("--------------------------------------------")
for i, file_name in enumerate(allfiles):
    file_vector = np.loadtxt(file_name)
    file_index_to_file_name[i] = file_name
    file_index_to_file_vector[i] = file_vector

    t.add_item(i, file_vector)
print("finished adding file vectors")

t.build(trees)
print("Step.1 - ANNOY index generation - Finished")
print("--- %.2f minutes passed ---------" % ((time.time() - start_time)/60))
print ("Step.2 - Similarity score calculation - Started ")
start_time = time.time()

named_nearest_neighbors = []
for i in file_index_to_file_name.keys():
    master_file_name = file_index_to_file_name[i]
    nn = {"filename": master_file_name.replace("\\", "/"), "similar": []}
    
    master_vector = file_index_to_file_vector[i]

    if i % 100 == 0:
        print("{}/{}--- {:.2f} minutes passed ---------".format(i, len(file_index_to_file_name), (time.time() - start_time)/60))
    
    nearest_neighbors = t.get_nns_by_item(i, n_nearest_neighbors)

    for j in nearest_neighbors:
        neighbor_file_name = file_index_to_file_name[j]
        neighbor_file_vector = file_index_to_file_vector[j]

        similarity = 1 - spatial.distance.cosine(master_vector, neighbor_file_vector)
        nn["similar"].append({"score": similarity, "filename": neighbor_file_name.replace("\\", "/")})
    named_nearest_neighbors.append(nn)
print("Step.3 - save result to file")
with open('nearest_neighbors.json', 'w') as outfile:
    json.dump(named_nearest_neighbors, outfile, sort_keys=True, indent=4)

print("completed")



