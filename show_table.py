import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)
cursor = conn.cursor()

cursor.execute("use patient")
cursor.execute("select * from symptoms_table")
data = cursor.fetchall()
for row in data:
    print(row)
cursor.execute("select * from patient_table")
data = cursor.fetchall()
for row in data:
    print(row)

conn.commit()
cursor.close()
conn.close()