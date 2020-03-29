import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

# load patients from csv file
def load_patients(path):
    file = pd.read_csv(path)
    return file

patients = load_patients("./PatientMatchingData.csv")

def levenshtein(seq1, seq2):
    # if either is null, return 0
    if pd.isna(seq1) or pd.isna(seq2)or seq1 == 'nan' or seq2 == 'nan':
        return 0
    
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
#     print (matrix)
    return (matrix[size_x - 1, size_y - 1])

# treat all columns (besides ID and account #'s) as alphabetic (ie string) for now
alphabeticCols = ['First Name', 'MI',
       'Last Name', 'Date of Birth', 'Sex', 'Current Street 1',
       'Current Street 2', 'Current City', 'Current State', 'Current Zip Code',
       'Previous First Name', 'Previous MI', 'Previous Last Name',
       'Previous Street 1', 'Previous Street 2', 'Previous City',
       'Previous State', 'Previous Zip Code']

patientsClean = patients.copy()

# make everything lowercase
for col in alphabeticCols:
    patientsClean.loc[:,col] = patientsClean.loc[:,col].astype(str).str.lower()
    
# make gender binary (0 for male 2 for female 1 for unknown) 1
# cleaning last and first name (removing digits, whitespace, and some special characters)
# cleaned current city by removing digits
for i in range(len(patientsClean)):
    patientsClean.loc[i, 'Last Name'] = re.sub('[\d\s~!@#%&:,]', '', patientsClean.loc[i,'Last Name'])
    patientsClean.loc[i, 'First Name'] = re.sub('[\d\s~!@#%&:,]', '', patientsClean.loc[i,'First Name'])
    patientsClean.loc[i, 'Sex'] = re.sub('[\d\s~!@#%&:,]', '', patientsClean.loc[i,'Sex'])
    patientsClean.loc[i, 'Sex'] = 0 if patientsClean.loc[i,'Sex'][0] == 'm' else 2 if patientsClean.loc[i,'Sex'][0] == 'f' else 1
    patientsClean.loc[i, 'Current City'] = re.sub('[\d~!@#%&:,]', '', patientsClean.loc[i, 'Current City'])

# verify if patient1 and patient2 are the same person
# need to determine optimal cutoffs (ie what levenshtein score is considered "different" enough to be 2 different people?)
def verify(patient1, patient2):
    numErrors = 0 # error considered as a field that is significantly different
    # consider first name
    compsMade = comparisons(patient1, patient2)
    if levenshtein(patient1['First Name'], patient2['First Name']) > 2:
        numErrors += 1
    # consider middle name
    if patient1['MI'] != 'nan' and patient2['MI'] != 'nan':
        if patient1['MI'][0] != patient2['MI'][0]:
            numErrors += 1
    # consider last name
    if levenshtein(patient1['Last Name'], patient2['Last Name']) > 2:
        numErrors += 1
    # consider DOB - more strict evaluation b/c less likely to mistype date of birth > 3 typos
    if levenshtein(patient1['Date of Birth'], patient2['Date of Birth']) > 3:
        # make sure there aren't any swapped character typos
        # TODO: swapped regex ?
        return False
    elif levenshtein(patient1['Date of Birth'], patient2['Date of Birth']) > 2:
        numErrors += 1
    # consider gender
    if abs(int(patient1['Sex']) - int(patient2['Sex'])) > 1:
        numErrors += 1
    # consider current street 1
    if levenshtein(patient1['Current Street 1'], patient2['Current Street 1']) > 3:
        numErrors += 1
    # consider current city
    if levenshtein(patient1['Current City'], patient2['Current City']) > 2:
        numErrors += 1
    # consider current zip
    if levenshtein(patient1['Current Zip Code'], patient2['Current Zip Code']) > 2:
            numErrors += 1
    # consider previous city
    if levenshtein(patient1['Previous City'], patient2['Previous City']) > 2:
        numErrors += 1
    # consider previous zip
    if levenshtein(patient1['Previous Zip Code'], patient2['Previous Zip Code']) > 2:
            numErrors += 1
    # different criteria depending on compsMade
    if compsMade > 7:
        return numErrors <= 2
    return numErrors <= 1

# take into account number of comparisons made
def comparisons(patient1, patient2):
    compsMade = 0
    if patient1['First Name'] != 'nan' and patient2['First Name'] != 'nan':
        compsMade += 1
    if patient1['Last Name'] != 'nan' and patient2['Last Name'] != 'nan':
        compsMade += 1
    if patient1['Date of Birth'] != 'nan' and patient2['Date of Birth'] != 'nan':
        compsMade += 1
    if patient1['Sex'] != 'nan' and patient2['Sex'] != 'nan':
        compsMade += 1
    if patient1['Current Street 1'] != 'nan' and patient2['Current Street 1'] != 'nan':
        compsMade += 1
    if patient1['Current City'] != 'nan' and patient2['Current City'] != 'nan':
        compsMade += 1
    if patient1['Current Zip Code'] != 'nan' and patient2['Current Zip Code'] != 'nan':
        compsMade += 1
    if patient1['Previous City'] != 'nan' and patient2['Previous City'] != 'nan':
        compsMade += 1
    if patient1['Previous Zip Code'] != 'nan' and patient2['Previous Zip Code'] != 'nan':
        compsMade += 1
    return compsMade

# Evaluation function to test accuracy and show stats
def run(patientClean):
    total = 0
    correct = 0
    falsePos = 0
    falseNeg = 0
    for index, patient in patientsClean.iterrows():
        for index1, patient1 in patientsClean.iterrows():
            if(index1 > index):
                result = verify(patient, patient1)
                ID1 = patient['GroupID']
                ID2 = patient1['GroupID']
                actual = ID1 == ID2
                if result == actual:
                    correct += 1
                elif result == True:
                    # print('false positive found between patients: ', patient['PatientID'], " and ", patient1['PatientID'])
                    falsePos += 1
                elif result == False:
                    # print('false negative found between patients: ', patient['PatientID'], " and ", patient1['PatientID'])
                    falseNeg += 1
                total += 1

    print("correct: ", correct)
    print("total: ", total)
    print("false positives: ", falsePos)
    print("false negatives: ", falseNeg)
    print("accuracy: ", correct/total)

    # Data to plot
    labels =["Correct","Incorrect"]
    sizes = [correct, total-correct]
    colors = ["lightblue","whitesmoke"]
    explode = (0.1,0)  # explode 1st slice
 
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Overall Accuracy')
    plt.show()

    # Data to plot
    labels =["False Positives","False Negatives"]
    sizes = [falsePos, falseNeg]
    colors = ["lightblue","whitesmoke"]
    explode = (0.1,0)  # explode 1st slice
    
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('False Positives and Negatives')
    plt.show()

run(patientsClean)

