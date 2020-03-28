import csv
import importlib  
leven = importlib.import_module("python-Levenshtein")
with open("PatientMatchingData.csv") as infile:
    reader = csv.reader(infile)
    reader = list(reader)
    data = reader[1:]

groups = {}     #partitioned groups
for line in data:
    lname = line[5].lower().strip()
    if lname in groups.keys():
        groups[lname].append((line[0],line[1]))
    else:
        groups[lname] = [(line[0],line[1])]

def accuracy(groups):
    err = 0
    keys = groups.keys()
    for key in keys:
        distinct = len(set(groups[key]))
        err += distinct - 1
    return err/201

print(len(groups.keys()))
print(accuracy(groups))

