import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)
cursor = conn.cursor()

cursor.execute("use patient")
cursor.execute("delete from symptoms_table")
cursor.execute("delete from patient_table")
print("tables are cleared now 😂")
conn.commit()
cursor.close()
conn.close()