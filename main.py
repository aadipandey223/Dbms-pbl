import mysql.connector

host = "localhost"
user = "root"
password = "password"
database = "patient"

def connect_db():
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

def gen_reg_id(conn):
    cur = conn.cursor()
    cur.execute("SELECT registration_id FROM patient_table ORDER BY registration_id DESC LIMIT 1")
    reg_id = cur.fetchone()
    cur.close()
    if reg_id is None:
        return "REG001"
    else:
        last_id_num = int(reg_id[0][3:])
        return f"REG{last_id_num + 1:03d}"

def insert_data(conn, name, gender, age, contact, registration_id):
    cur = conn.cursor()
    sql = "INSERT INTO patient_table (registration_id, name, gender, age, contact) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (registration_id, name, gender, age, contact))
    conn.commit()
    cur.close()
    print(f"✅ Your info has been recorded. Your Registration ID is: {registration_id}")

def record_symptoms(conn, registration_id):
    cur = conn.cursor()

    # Get list of symptom columns
    cur.execute("SHOW COLUMNS FROM symptoms_table")
    columns = [row[0] for row in cur.fetchall()]
    symptom_columns = [col for col in columns if col != 'registration_id']

    print("\nNow tell me your symptoms one by one (e.g. I have fever). Type 'done' or 'no' when finished.")
    exit_keywords = {'no', 'ok', 'done', 'that\'s it', 'nothing'}

    while True:
        user_input = input(">> ").strip().lower()
        if user_input in exit_keywords:
            break

        matched = False
        for col in symptom_columns:
            if col.replace('_', ' ') in user_input or col in user_input:
                sql = f"UPDATE symptoms_table SET {col} = 1 WHERE registration_id = %s"
                cur.execute(sql, (registration_id,))
                conn.commit()
                print("OK and❓")
                matched = True
                break

        if not matched:
            print("❌ No matching symptom found in database columns.")

    cur.close()
    print("✅ Symptom recording completed.")

def main():
    try:
        conn = connect_db()

        reg_id = gen_reg_id(conn)

        print("Enter Patient Details:")
        name = input("Enter Name: ")
        gender = input("Enter Gender: ")
        age = int(input("Enter Age: "))
        contact = input("Enter Contact Number: ")

        insert_data(conn, name, gender, age, contact, reg_id)

        # Initialize symptoms row with registration ID
        cur = conn.cursor()
        cur.execute("INSERT INTO symptoms_table (registration_id) VALUES (%s)", (reg_id,))
        conn.commit()
        cur.close()

        record_symptoms(conn, reg_id)

        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    main()

def function_name():
    pass  # Placeholder for any additional functions you may want to add later    