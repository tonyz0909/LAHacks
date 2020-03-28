import csv
with open("PatientMatchingData.csv") as infile:
    reader = csv.reader(infile)
    reader = list(reader)
    data = reader[1:]

groups = {}
for line in data:
    lname = line[5].lower().strip()
    if lname in groups.keys():
        groups[lname].append((line[0],line[1]))
    else:
        groups[lname] = [(line[0],line[1])]

print(len(groups.keys()))   

