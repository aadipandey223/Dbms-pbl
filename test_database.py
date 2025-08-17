import mysql.connector

def test_database():
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="patient"
        )
        cursor = conn.cursor()
        
        print("✅ Database connection successful!")
        print("\n" + "="*50)
        
        # Test 1: Check if all tables exist
        print("📋 Checking tables...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n" + "="*50)
        
        # Test 2: Check diseases
        print("🦠 Checking diseases...")
        cursor.execute("SELECT * FROM disease LIMIT 5")
        diseases = cursor.fetchall()
        print(f"Found {len(diseases)} diseases:")
        for disease in diseases:
            print(f"  - ID: {disease[0]}, Name: {disease[1]}")
        
        print("\n" + "="*50)
        
        # Test 3: Check disease-symptom mappings
        print("🔍 Checking disease-symptom mappings...")
        cursor.execute("SELECT d.disease_name, ds.symptom_name FROM disease d JOIN disease_symptom ds ON d.disease_id = ds.disease_id WHERE d.disease_name = 'Pneumonia'")
        mappings = cursor.fetchall()
        print("Pneumonia symptoms:")
        for mapping in mappings:
            print(f"  - {mapping[1]}")
        
        print("\n" + "="*50)
        
        # Test 4: Check medicines
        print("💊 Checking medicines...")
        cursor.execute("SELECT m.medicine_name, m.dosage, d.disease_name FROM medicines m JOIN disease d ON m.disease_id = d.disease_id WHERE d.disease_name = 'COVID-19'")
        medicines = cursor.fetchall()
        print("COVID-19 medicines:")
        for medicine in medicines:
            print(f"  - {medicine[0]} ({medicine[1]})")
        
        print("\n" + "="*50)
        
        # Test 5: Check precautions
        print("🛡️ Checking precautions...")
        cursor.execute("SELECT p.precaution_text, d.disease_name FROM precautions p JOIN disease d ON p.disease_id = d.disease_id WHERE d.disease_name = 'Dengue Fever'")
        precautions = cursor.fetchall()
        print("Dengue Fever precautions:")
        for precaution in precautions:
            print(f"  - {precaution[0]}")
        
        print("\n" + "="*50)
        print("✅ Database setup completed successfully!")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_database()
