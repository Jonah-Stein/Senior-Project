# Purpose is to take .soi and .toi data from pref-lib files and aggregate the data into a single csv
# That csv will then be used for later to determine the probabilistic truncation model
import os
import csv

fields = ["Dataset", "Title", "Alternatives", "Voters", "Ballot Lengths"]
data_file = open('empiricaldata.csv', 'w')
data_writer = csv.DictWriter(data_file, fieldnames = fields)
data_writer.writeheader()

unpackaged_data = []
empirical_data = os.scandir('empirical data')
# for x in empirical_data: 
#     print(x.path)
# f = open("00030-00000001.soi", "r")
# dict_data = dict()
# ballot_lengths = list()
elections = []
alternative_numbers = [0] * 15
counter = 0
for file in empirical_data:
    if ".soi" not in file.path and ".toi" not in file.path:
        continue
    data = open(file.path, 'r')
    dict_data = dict()
    ballot_lengths = list()
    counter += 1
    for x in data:
        if x[0] == '#':
            if "FILE NAME" in x:
                dict_data["Dataset"] = x.split(": ")[1].split("-")[0]
                if dict_data["Dataset"] not in elections:
                    elections.append(dict_data["Dataset"])
            elif "TITLE" in x:
                dict_data["Title"] = x.split(": ")[1].replace('\n', '')
            elif "ALTERNATIVES" in x:
                dict_data["Alternatives"] = int(x.split(": ")[1])
                ballot_lengths = [0] * dict_data["Alternatives"]
                alternative_numbers[dict_data["Alternatives"]] += 1
            elif "VOTERS" in x:
                dict_data["Voters"] = int(x.split(": ")[1])
            continue
        else:
            voters = int(x.split(': ')[0])
            candidates_ranked = len(x.split(': ')[1].split(','))
            ballot_lengths[candidates_ranked - 1] += voters

    dict_data["Ballot Lengths"] = ballot_lengths
    unpackaged_data.append(dict_data)

prob_model_4 = [0] * 4
prob_model_5 = [0] * 5
prob_model_6 = [0] * 6
prob_model_7 = [0] * 7

for election in unpackaged_data:
    if election["Alternatives"] == 4:
        prob_model_4 = [x + y for x, y in zip(prob_model_4, election["Ballot Lengths"])]
    if election["Alternatives"] == 5:
        prob_model_5 = [x + y for x, y in zip(prob_model_5, election["Ballot Lengths"])]
    if election["Alternatives"] == 6:
        prob_model_6 = [x + y for x, y in zip(prob_model_6, election["Ballot Lengths"])]
    if election["Alternatives"] == 7:
        prob_model_7 = [x + y for x, y in zip(prob_model_7, election["Ballot Lengths"])]

def convert_to_percentages(prob_model):
    total = sum(prob_model)
    prob_model = [x / total for x in prob_model]
    return prob_model
# print(prob_model_4)
# print(convert_to_percentages(prob_model_4))
f = open("Final Probability Models", "w")
f.write(f"4: {convert_to_percentages(prob_model_4)}\n")
f.write(f"5: {convert_to_percentages(prob_model_5)}\n")
f.write(f"6: {convert_to_percentages(prob_model_6)}\n")
f.write(f"7: {convert_to_percentages(prob_model_7)}\n")
f.close()
# data_writer.writerows(unpackaged_data)
print(counter)
print(elections)
print(alternative_numbers)