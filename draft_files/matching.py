import csv
import re
import importlib  
# leven = importlib.import_module("python-Levenshtein")
with open("PatientMatchingData.csv") as infile:
    reader = csv.reader(infile)
    reader = list(reader)
    data = reader[1:]

# groups = dictionary with key: criterion, value: group_id

# 1. check by lname
def lname():
    groups = {}     #partitioned groups
    for line in data:
        lname = line[5].lower().strip()
        if lname in groups.keys():
            groups[lname].append(line[0])
        else:
            groups[lname] = [line[0]]
    return groups

# 2. multiple criterion (lname, dob, address) pts based system
def mult3():
    groups = {}
    for line in data:
        lname = line[5].lower().strip()
        dob = line[6]
        address = line[8].lower().strip()
        if len(groups) == 0:
            groups[(lname, dob, address)] = [line[0]]
        else:
            for key in groups.keys():
                pts = 0
                if lname in key:
                    pts += 1
                if dob in key:
                    pts += 1
                if address in key:
                    pts += 1
                if pts >= 2:
                    groups[key].append(line[0])
                    break
            if pts < 2:
                groups[(lname, dob, address)] = [line[0]]
    return groups

# checked between address and zipcode also
def mult4():
    groups = {}
    for line in data:
        lname = line[5].lower().strip()
        dob = line[6]
        address = line[8].lower().strip()
        zipcode = line[12]
        if len(groups) == 0:
            groups[(lname, dob, address, zipcode)] = [line[0]]
        else:
            for key in groups.keys():
                pts = 0
                if lname in key:
                    pts += 1
                if dob in key:
                    pts += 1
                if address != '' and address in key or zipcode != '' and zipcode in key:
                    pts += 1
                if pts >= 2:
                    groups[key].append(line[0])
                    break
            if pts < 2:
                groups[(lname, dob, address, zipcode)] = [line[0]]
    return groups

# name handles typos (checks first and last letters)
def multadj():
    groups = {}
    for line in data:
        l_reg = '' if len(line[5].strip()) < 2 else line[5].lower()[0] + line[5].lower()[-1]
        dob = line[6]
        address = line[8].lower().strip()
        zipcode = line[12]
        if len(groups) == 0:
            groups[(l_reg, dob, address)] = [line[0]]
        else:
            for key in groups.keys():
                pts = 0
                if l_reg in key:
                    pts += 1
                if dob in key:
                    pts += 1
                if address != '' and address in key:
                    pts += 1
                if pts >= 2:
                    groups[key].append(line[0])
                    break
            if pts < 2:
                groups[(l_reg, dob, address)] = [line[0]]
    return groups

# helper methods to check accuracy (approximate) +- 2.5% for this data
def accuracy(groups):
    err = 0
    keys = groups.keys()
    for key in keys:
        distinct = len(set(groups[key]))
        err += distinct - 1
    err += abs(len(groups) - 65)
    return 1-err/201

def info(groups):
    err = 0
    keys = groups.keys()
    for key in keys:
        distinct = len(set(groups[key]))
        err += distinct - 1
    org = err
    err += abs(len(groups) - 65)
    return f'Accuracy: {1-err/201}, # groups: {len(groups)}, overmatches: {org}, undermatches: {err-org}'

group1 = lname()
group2 = mult3()
group3 = mult4()
group4 = multadj()
print(info(group1))
print(info(group2))
print(info(group3))
print(info(group4))
print(group4)
