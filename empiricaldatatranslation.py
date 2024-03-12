# Purpose is to take .soi and .toi data from pref-lib files and aggregate the data into a single csv
# That csv will then be used for later to determine the probabilistic truncation model

import csv

data_file = open('empiricaldata.csv', 'w')
data_writer = csv.writer(data_file)

f = open("00030-00000001.soi", "r")
dict_data = dict()
ballot_lengths = list()
for x in f:
    if x[0] == '#':
        if "ALTERNATIVES" in x:
            dict_data["Alternatives"] = int(x.split(": ")[1])
            ballot_lengths = [0] * dict_data["Alternatives"]
        if "VOTERS" in x:
            dict_data["Voters"] = int(x.split(": ")[1])
        continue
    else:
        voters = int(x.split(': ')[0])
        candidates_ranked = len(x.split(': ')[1].split(','))
        ballot_lengths[candidates_ranked - 1] += voters
        print(voters, candidates_ranked)

dict_data["Ballot Lengths"] = ballot_lengths
print(dict_data)
#print(f.read())