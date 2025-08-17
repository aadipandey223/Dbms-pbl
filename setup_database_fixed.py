import mysql.connector

def setup_database():
    try:
        # First, connect without specifying database to create it
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )
        cursor = conn.cursor()
        
        print("✅ Connected to MySQL server")
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS patient")
        cursor.execute("USE patient")
        print("✅ Database 'patient' created/selected")
        
        # Create tables
        print("📋 Creating tables...")
        
        # Patient table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_table (
                registration_id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100),
                gender VARCHAR(10),
                age INT,
                contact VARCHAR(15)
            )
        """)
        
        # Symptoms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms_table (
                registration_id VARCHAR(20) PRIMARY KEY,
                fever BOOLEAN DEFAULT 0,
                high_fever BOOLEAN DEFAULT 0,
                mild_fever BOOLEAN DEFAULT 0,
                chills BOOLEAN DEFAULT 0,
                fatigue BOOLEAN DEFAULT 0,
                weakness BOOLEAN DEFAULT 0,
                body_ache BOOLEAN DEFAULT 0,
                body_pain BOOLEAN DEFAULT 0,
                night_sweats BOOLEAN DEFAULT 0,
                sweating BOOLEAN DEFAULT 0,
                weight_loss BOOLEAN DEFAULT 0,
                dry_cough BOOLEAN DEFAULT 0,
                wet_cough BOOLEAN DEFAULT 0,
                persistent_cough BOOLEAN DEFAULT 0,
                blood_in_cough BOOLEAN DEFAULT 0,
                chest_pain BOOLEAN DEFAULT 0,
                chest_tightness BOOLEAN DEFAULT 0,
                breathing_difficulty BOOLEAN DEFAULT 0,
                fast_breathing BOOLEAN DEFAULT 0,
                sore_throat BOOLEAN DEFAULT 0,
                runny_nose BOOLEAN DEFAULT 0,
                sneezing BOOLEAN DEFAULT 0,
                nasal_congestion BOOLEAN DEFAULT 0,
                nausea BOOLEAN DEFAULT 0,
                vomiting BOOLEAN DEFAULT 0,
                diarrhea BOOLEAN DEFAULT 0,
                constipation BOOLEAN DEFAULT 0,
                stomach_pain BOOLEAN DEFAULT 0,
                stomach_cramps BOOLEAN DEFAULT 0,
                loss_of_appetite BOOLEAN DEFAULT 0,
                appetite_loss BOOLEAN DEFAULT 0,
                dehydration BOOLEAN DEFAULT 0,
                dizziness BOOLEAN DEFAULT 0,
                headache BOOLEAN DEFAULT 0,
                confusion BOOLEAN DEFAULT 0,
                rash BOOLEAN DEFAULT 0,
                skin_rash BOOLEAN DEFAULT 0,
                skin_blisters BOOLEAN DEFAULT 0,
                red_eyes BOOLEAN DEFAULT 0,
                watery_eyes BOOLEAN DEFAULT 0,
                itchy_eyes BOOLEAN DEFAULT 0,
                itchy_throat BOOLEAN DEFAULT 0,
                eye_pain BOOLEAN DEFAULT 0,
                ear_pain BOOLEAN DEFAULT 0,
                bleeding_gums BOOLEAN DEFAULT 0,
                low_platelet BOOLEAN DEFAULT 0,
                difficulty_swallowing BOOLEAN DEFAULT 0,
                swollen_tonsils BOOLEAN DEFAULT 0,
                white_spots_mouth BOOLEAN DEFAULT 0,
                FOREIGN KEY (registration_id) REFERENCES patient_table(registration_id)
            )
        """)
        
        # Disease table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disease (
                disease_id INT PRIMARY KEY AUTO_INCREMENT,
                disease_name VARCHAR(100),
                description TEXT
            )
        """)
        
        # Disease-symptom mapping table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disease_symptom (
                disease_id INT,
                symptom_name VARCHAR(50),
                FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
            )
        """)
        
        # Medicines table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                medicine_id INT PRIMARY KEY AUTO_INCREMENT,
                medicine_name VARCHAR(100),
                dosage VARCHAR(100),
                disease_id INT,
                FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
            )
        """)
        
        # Precautions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS precautions (
                precaution_id INT PRIMARY KEY AUTO_INCREMENT,
                precaution_text TEXT,
                disease_id INT,
                FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
            )
        """)
        
        print("✅ All tables created successfully")
        
        # Insert sample diseases
        print("🦠 Inserting diseases...")
        diseases = [
            ('Pneumonia', 'Infection that inflames air sacs in lungs'),
            ('COVID-19', 'Respiratory illness caused by coronavirus'),
            ('Dengue Fever', 'Viral infection transmitted by mosquitoes'),
            ('Common Cold', 'Viral upper respiratory tract infection'),
            ('Bronchial Asthma', 'Chronic respiratory condition with airway inflammation'),
            ('Gastroenteritis', 'Inflammation of stomach and intestines'),
            ('Migraine', 'Severe recurring headache'),
            ('Conjunctivitis', 'Inflammation of the eye conjunctiva'),
            ('Tonsillitis', 'Inflammation of tonsils'),
            ('Urinary Tract Infection', 'Infection in urinary system')
        ]
        
        cursor.executemany("INSERT INTO disease (disease_name, description) VALUES (%s, %s)", diseases)
        print(f"✅ Inserted {len(diseases)} diseases")
        
        # Insert disease-symptom mappings
        print("🔍 Inserting disease-symptom mappings...")
        mappings = [
            # Pneumonia
            (1, 'fever'), (1, 'high_fever'), (1, 'dry_cough'), (1, 'chest_pain'),
            (1, 'breathing_difficulty'), (1, 'fatigue'), (1, 'chills'), (1, 'sweating'),
            
            # COVID-19
            (2, 'fever'), (2, 'dry_cough'), (2, 'fatigue'), (2, 'body_ache'),
            (2, 'sore_throat'), (2, 'headache'), (2, 'loss_of_appetite'), (2, 'diarrhea'),
            
            # Dengue Fever
            (3, 'high_fever'), (3, 'headache'), (3, 'body_pain'), (3, 'rash'),
            (3, 'low_platelet'), (3, 'nausea'), (3, 'vomiting'), (3, 'fatigue'),
            
            # Common Cold
            (4, 'mild_fever'), (4, 'runny_nose'), (4, 'sneezing'), (4, 'sore_throat'),
            (4, 'dry_cough'), (4, 'nasal_congestion'), (4, 'fatigue'),
            
            # Bronchial Asthma
            (5, 'breathing_difficulty'), (5, 'chest_tightness'), (5, 'persistent_cough'),
            (5, 'fatigue'),
            
            # Gastroenteritis
            (6, 'nausea'), (6, 'vomiting'), (6, 'diarrhea'), (6, 'stomach_pain'),
            (6, 'loss_of_appetite'), (6, 'dehydration'), (6, 'fever'),
            
            # Migraine
            (7, 'headache'), (7, 'nausea'), (7, 'dizziness'),
            
            # Conjunctivitis
            (8, 'red_eyes'), (8, 'watery_eyes'), (8, 'itchy_eyes'), (8, 'eye_pain'),
            
            # Tonsillitis
            (9, 'sore_throat'), (9, 'difficulty_swallowing'), (9, 'swollen_tonsils'),
            (9, 'fever'), (9, 'headache'), (9, 'white_spots_mouth'),
            
            # UTI
            (10, 'fever'), (10, 'nausea')
        ]
        
        cursor.executemany("INSERT INTO disease_symptom (disease_id, symptom_name) VALUES (%s, %s)", mappings)
        print(f"✅ Inserted {len(mappings)} symptom mappings")
        
        # Insert sample medicines
        print("💊 Inserting medicines...")
        medicines = [
            ('Azithromycin', '500mg once daily for 3-5 days', 1),
            ('Amoxicillin', '500mg three times daily for 7-10 days', 1),
            ('Acetaminophen', '500-1000mg every 4-6 hours as needed', 2),
            ('Ibuprofen', '400-600mg every 4-6 hours as needed', 2),
            ('Acetaminophen', '500-1000mg every 4-6 hours as needed', 3),
            ('Dextromethorphan', '30mg every 4-6 hours as needed', 4),
            ('Albuterol Inhaler', '90mcg/puff as needed', 5),
            ('Loperamide', '2mg after each loose stool', 6),
            ('Sumatriptan', '50-100mg as needed', 7),
            ('Chloramphenicol Eye Drops', '1-2 drops every 2-4 hours', 8),
            ('Penicillin V', '500mg four times daily for 10 days', 9),
            ('Nitrofurantoin', '100mg twice daily for 5-7 days', 10)
        ]
        
        cursor.executemany("INSERT INTO medicines (medicine_name, dosage, disease_id) VALUES (%s, %s, %s)", medicines)
        print(f"✅ Inserted {len(medicines)} medicines")
        
        # Insert sample precautions
        print("🛡️ Inserting precautions...")
        precautions = [
            ('Consult doctor immediately', 1),
            ('Take prescribed medication as directed', 1),
            ('Rest and stay hydrated', 1),
            ('Isolate yourself from others', 2),
            ('Monitor symptoms closely', 2),
            ('Stay hydrated and rest', 2),
            ('Avoid NSAIDs (use only acetaminophen)', 3),
            ('Stay hydrated with oral rehydration solution', 3),
            ('Rest and avoid strenuous activity', 3),
            ('Rest and stay hydrated', 4),
            ('Use over-the-counter medications as directed', 4),
            ('Avoid triggers (dust, smoke, pollen)', 5),
            ('Keep rescue inhaler with you', 5),
            ('Stay hydrated with clear fluids', 6),
            ('Eat bland foods (BRAT diet)', 6),
            ('Rest in a quiet, dark room', 7),
            ('Avoid trigger foods', 7),
            ('Avoid touching or rubbing eyes', 8),
            ('Wash hands frequently', 8),
            ('Rest voice and throat', 9),
            ('Stay hydrated with warm liquids', 9),
            ('Drink plenty of water', 10),
            ('Urinate frequently', 10)
        ]
        
        cursor.executemany("INSERT INTO precautions (precaution_text, disease_id) VALUES (%s, %s)", precautions)
        print(f"✅ Inserted {len(precautions)} precautions")
        
        conn.commit()
        print("✅ All data inserted successfully!")
        
        # Test the setup
        test_connection(cursor)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_connection(cursor):
    print("\n🔍 Testing database setup...")
    
    # Check tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"✅ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check data counts
    cursor.execute("SELECT COUNT(*) FROM disease")
    disease_count = cursor.fetchone()[0]
    print(f"✅ Found {disease_count} diseases")
    
    cursor.execute("SELECT COUNT(*) FROM medicines")
    medicine_count = cursor.fetchone()[0]
    print(f"✅ Found {medicine_count} medicines")
    
    cursor.execute("SELECT COUNT(*) FROM precautions")
    precaution_count = cursor.fetchone()[0]
    print(f"✅ Found {precaution_count} precautions")
    
    print("\n🎉 Database setup completed successfully!")

if __name__ == "__main__":
    setup_database()
