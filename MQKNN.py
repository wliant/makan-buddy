import numpy as np
import operator

class MQKNN:
    def __init__(self, dims, K, data_files, query_files, W):
        self.dims = dims
        print("data size: {}".format(len(data_files)))
        print("query size: {}".format(len(query_files)))
        self.K = K
        self.X = []
        self.file_name_mapping = {}
        self.W = W
        for i , file_name in enumerate(data_files):
            self.file_name_mapping[i] = file_name
            self.X.append(np.loadtxt(file_name))

        self.Q = []
        for file_name in query_files:
            self.Q.append(np.loadtxt(file_name))

        self.__calc_delta_ijl()
        self.__calc_KS_l_prime()
        self.__calc_KS_l()
        self.__calc_B_i()
        self.__calc_MSD_i()
    
    def __calc_delta_ijl(self):
        self.delt = []
        for l in range(0, self.dims):
            delt_l = []
            for j in range(0, len(self.Q)):
                delt_j = []
                for i in range(0, len(self.X)):
                    delta_value = self.W[j]*abs(self.X[i][l]-self.Q[j][l])
                    delt_j.append((i, delta_value))
                delt_l.append(delt_j)
            self.delt.append(delt_l)

    def __calc_KS_l_prime(self):
        self.KS_l_prime = []
        for l in range(0, self.dims):
            counter = {}
            for j in range(0, len(self.Q)):
                self.delt[l][j].sort(key = operator.itemgetter(1))
                for id, dist in [self.delt[l][j][k] for k in range(0, self.K)]:
                    if id in counter:
                        val = counter[id]
                        counter[id] = (val[0]+1, val[1]+dist)
                    else:
                        counter[id] = (1, dist)
            self.KS_l_prime.append(counter)

    def __calc_KS_l(self):
        self.KS_l = []
        for l in range(0, self.dims):
            st = sorted(self.KS_l_prime[l].items(), key=lambda x: (-x[1][0], x[1][1]))
            self.KS_l.append(set([st[k][0] for k in range(0, self.K)]))
    
    def __calc_B_i(self):
        self.B_i = []
        for i in range(0, len(self.X)):
            self.B_i.append([1 if i in self.KS_l[l] else 0 for l in range(0, self.dims)])

    def q_bar_l(self, l):
        nominator = 0
        denominator = 0
        for j in range(0, len(self.Q)):
            nominator += self.W[j] * self.Q[j][l]
            denominator += self.W[j]
        return nominator / denominator

    def __calc_MSD_i(self):
        self.MSD_i = []
        for i in range(0, len(self.X)):
            nominator = 0
            denominator = 0
            for l in range(0, self.dims):
                if self.B_i[i][l] != 0:
                    nominator += abs(self.X[i][l] - self.q_bar_l(l))
                    denominator += 1
            denominator = denominator **2
            self.MSD_i.append((i, nominator/denominator if denominator > 0 else float('inf')))

    def get_result(self):
        st = sorted(self.MSD_i, key = lambda x: x[1])
        top_k = [st[k] for k in range(0, self.K)]
        return [self.file_name_mapping[t[0]] for t in top_k]
        
