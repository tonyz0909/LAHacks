import pymysql
import csv
connection = pymysql.connect(host = 'localhost', user = 'root', password = 'admin',
# connection = pymysql.connect(host = 'localhost', user = 'root', 
    db = 'PatientMatching', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
with open("PatientMatchingData.csv") as infile:
    reader = csv.reader(infile)
    reader = list(reader)
    data = reader[1:]

with connection.cursor() as cursor:
    cursor.execute("use PatientMatching;")
    statement = "Insert into patients values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(statement, data)
    connection.commit()

connection.close()
