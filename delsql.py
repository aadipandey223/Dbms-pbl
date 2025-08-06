import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)
cursor = conn.cursor()

cursor.execute("SHOW DATABASES")
system_dbs = ['mysql', 'information_schema', 'performance_schema', 'sys']

for (db_name,) in cursor.fetchall():
    if db_name not in system_dbs:
        try:
            cursor.execute(f"DROP DATABASE `{db_name}`")
            print(f"Dropped database: {db_name}")
        except mysql.connector.Error as err:
            print(f"Failed to drop {db_name}: {err}")

cursor.close()
conn.close()
