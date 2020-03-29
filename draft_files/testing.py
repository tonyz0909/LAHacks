import csv

with open("PatientMatchingData.csv") as infile:
    reader = csv.reader(infile)
    reader = list(reader)
    data = reader[1:]

def check(p1, p2):
    pts = 0
    lname1, lname2 = p1[5].lower().strip(), p2[5].lower().strip()
    # finit1 = '' if len(p1[3]) < 2 else p1[3].lower().strip()[0] + p1[3].lower().strip()[-1]
    # finit2 = '' if len(p2[3]) < 2 else p2[3].lower().strip()[0] + p2[3].lower().strip()[-1]
    # linit1 = '' if len(p1[5]) < 2 else p1[5].lower().strip()[0] + p1[5].lower().strip()[-1]
    # linit2 = '' if len(p2[5]) < 2 else p2[5].lower().strip()[0] + p2[5].lower().strip()[-1]
    dob1, dob2 = p1[6], p2[6]
    address1, address2 = p1[8].lower().strip(), p2[8].lower().strip()
    zip1, zip2 = p1[12], p2[12]
    if lname1 == lname2:
        pts += 1
    if dob1 == dob2:
        pts += 1
    if address1 == address2 or zip1 == zip2:
        pts += 1
    if pts >= 2:
        return True
    return False

def accuracy():
    correct = 0
    wrong = 0
    falseNeg = 0
    falsePos = 0
    for i in range(len(data)-1):
        for j in range(i+1, len(data)):
            p1 = data[i]
            p2 = data[j]
            actual = p1[0] == p2[0]
            predicted = check(p1, p2)
            if predicted == actual:
                correct += 1
            elif predicted == True:
                falsePos += 1
                wrong += 1
            elif predicted == False:
                falseNeg += 1
                wrong += 1
    return [correct/(correct + wrong), correct, wrong, falseNeg, falsePos]

print(accuracy())