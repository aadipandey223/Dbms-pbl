import mysql.connector

def enhance_database():
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="patient"
        )
        cursor = conn.cursor()
        
        print("🔧 Enhancing database with new features...")
        
        # 1. Create consultations table
        print("📝 Creating consultations table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                consultation_id INT PRIMARY KEY AUTO_INCREMENT,
                patient_id VARCHAR(10),
                consultation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                symptoms_analyzed TEXT,
                diagnosis_results TEXT,
                confidence_score DECIMAL(5,2),
                doctor_notes TEXT,
                follow_up_date DATE,
                status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
                FOREIGN KEY (patient_id) REFERENCES patient_table(registration_id)
            )
        """)
        print("✅ Consultations table created")
        
        # 2. Create user accounts table
        print("👤 Creating user accounts table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_accounts (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'doctor', 'nurse', 'patient') DEFAULT 'patient',
                full_name VARCHAR(100) NOT NULL,
                specialization VARCHAR(100),
                license_number VARCHAR(50),
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL
            )
        """)
        print("✅ User accounts table created")
        
        # 3. Create patient_doctors table for relationships
        print("🔗 Creating patient-doctor relationships table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_doctors (
                relationship_id INT PRIMARY KEY AUTO_INCREMENT,
                patient_id VARCHAR(10),
                doctor_id INT,
                assigned_date DATE DEFAULT (CURRENT_DATE),
                is_active BOOLEAN DEFAULT 1,
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patient_table(registration_id),
                FOREIGN KEY (doctor_id) REFERENCES user_accounts(user_id)
            )
        """)
        print("✅ Patient-doctor relationships table created")
        
        # 4. Create treatment_plans table
        print("💊 Creating treatment plans table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treatment_plans (
                plan_id INT PRIMARY KEY AUTO_INCREMENT,
                consultation_id INT,
                disease_id INT,
                treatment_description TEXT,
                medications_prescribed TEXT,
                dosage_instructions TEXT,
                duration_days INT,
                created_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('active', 'completed', 'discontinued') DEFAULT 'active',
                FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id),
                FOREIGN KEY (disease_id) REFERENCES disease(disease_id),
                FOREIGN KEY (created_by) REFERENCES user_accounts(user_id)
            )
        """)
        print("✅ Treatment plans table created")
        
        # 5. Create symptoms_severity table
        print("📊 Creating symptoms severity table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms_severity (
                severity_id INT PRIMARY KEY AUTO_INCREMENT,
                consultation_id INT,
                symptom_name VARCHAR(50),
                severity_level ENUM('mild', 'moderate', 'severe') DEFAULT 'moderate',
                notes TEXT,
                FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id)
            )
        """)
        print("✅ Symptoms severity table created")
        
        # 6. Insert sample admin user
        print("👨‍⚕️ Creating sample admin user...")
        cursor.execute("""
            INSERT INTO user_accounts (username, email, password_hash, role, full_name, specialization, license_number)
            VALUES ('admin', 'admin@medicare.com', 'admin123', 'admin', 'System Administrator', 'System Management', 'ADMIN001')
            ON DUPLICATE KEY UPDATE username=username
        """)
        
        # 7. Insert sample doctor
        cursor.execute("""
            INSERT INTO user_accounts (username, email, password_hash, role, full_name, specialization, license_number)
            VALUES ('dr.smith', 'dr.smith@medicare.com', 'doctor123', 'doctor', 'Dr. John Smith', 'General Medicine', 'MD001')
            ON DUPLICATE KEY UPDATE username=username
        """)
        
        # 8. Insert sample nurse
        cursor.execute("""
            INSERT INTO user_accounts (username, email, password_hash, role, full_name, specialization, license_number)
            VALUES ('nurse.jones', 'nurse.jones@medicare.com', 'nurse123', 'nurse', 'Nurse Sarah Jones', 'Emergency Care', 'RN001')
            ON DUPLICATE KEY UPDATE username=username
        """)
        
        print("✅ Sample users created")
        
        # 9. Add more diseases
        print("🦠 Adding more diseases...")
        additional_diseases = [
            ('Hypertension', 'High blood pressure condition'),
            ('Diabetes Type 2', 'Metabolic disorder affecting blood sugar'),
            ('Migraine', 'Severe recurring headache with neurological symptoms'),
            ('Gastritis', 'Inflammation of stomach lining'),
            ('Sinusitis', 'Inflammation of sinuses'),
            ('Bronchitis', 'Inflammation of bronchial tubes'),
            ('Urinary Tract Infection', 'Bacterial infection in urinary system'),
            ('Conjunctivitis', 'Inflammation of eye conjunctiva'),
            ('Dermatitis', 'Skin inflammation and irritation'),
            ('Anxiety Disorder', 'Mental health condition with excessive worry')
        ]
        
        cursor.executemany("""
            INSERT INTO disease (disease_name, description) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE disease_name=disease_name
        """, additional_diseases)
        print(f"✅ Added {len(additional_diseases)} more diseases")
        
        # 10. Add more disease-symptom mappings
        print("🔍 Adding more disease-symptom mappings...")
        additional_mappings = [
            # Hypertension
            (11, 'headache'), (11, 'dizziness'), (11, 'chest_pain'), (11, 'fatigue'),
            
            # Diabetes Type 2
            (12, 'fatigue'), (12, 'weight_loss'),
            
            # Migraine
            (13, 'headache'), (13, 'nausea'), (13, 'dizziness'),
            
            # Gastritis
            (14, 'stomach_pain'), (14, 'nausea'), (14, 'vomiting'), (14, 'loss_of_appetite'),
            
            # Sinusitis
            (15, 'nasal_congestion'), (15, 'headache'),
            
            # Bronchitis
            (16, 'persistent_cough'), (16, 'chest_pain'), (16, 'fatigue'), (16, 'mild_fever'),
            
            # UTI
            (17, 'fever'), (17, 'nausea'),
            
            # Conjunctivitis
            (18, 'red_eyes'), (18, 'watery_eyes'), (18, 'itchy_eyes'), (18, 'eye_pain'),
            
            # Dermatitis
            (19, 'rash'), (19, 'skin_rash'), (19, 'itchy_eyes'), (19, 'skin_blisters'),
            
            # Anxiety Disorder
            (20, 'fatigue')
        ]
        
        cursor.executemany("""
            INSERT INTO disease_symptom (disease_id, symptom_name) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE disease_id=disease_id
        """, additional_mappings)
        print(f"✅ Added {len(additional_mappings)} more symptom mappings")
        
        # 11. Add more medicines
        print("💊 Adding more medicines...")
        additional_medicines = [
            ('Amlodipine', '5-10mg once daily', 11),
            ('Metformin', '500-1000mg twice daily', 12),
            ('Sumatriptan', '50-100mg as needed', 13),
            ('Omeprazole', '20-40mg once daily', 14),
            ('Fluticasone', '50mcg twice daily', 15),
            ('Azithromycin', '500mg once daily for 3 days', 16),
            ('Nitrofurantoin', '100mg twice daily for 5 days', 17),
            ('Chloramphenicol', '1-2 drops every 2-4 hours', 18),
            ('Hydrocortisone', '1% cream applied 2-3 times daily', 19),
            ('Sertraline', '50-100mg once daily', 20)
        ]
        
        cursor.executemany("""
            INSERT INTO medicines (medicine_name, dosage, disease_id) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE medicine_name=medicine_name
        """, additional_medicines)
        print(f"✅ Added {len(additional_medicines)} more medicines")
        
        # 12. Add more precautions
        print("🛡️ Adding more precautions...")
        additional_precautions = [
            ('Monitor blood pressure regularly', 11),
            ('Reduce salt intake', 11),
            ('Exercise regularly', 11),
            ('Monitor blood sugar levels', 12),
            ('Follow diabetic diet', 12),
            ('Exercise regularly', 12),
            ('Avoid trigger foods', 13),
            ('Manage stress', 13),
            ('Avoid spicy foods', 14),
            ('Eat smaller meals', 14),
            ('Use saline nasal spray', 15),
            ('Stay hydrated', 15),
            ('Rest and stay hydrated', 16),
            ('Avoid smoking', 16),
            ('Drink plenty of water', 17),
            ('Urinate frequently', 17),
            ('Avoid touching eyes', 18),
            ('Wash hands frequently', 18),
            ('Avoid irritants', 19),
            ('Keep skin moisturized', 19),
            ('Practice relaxation techniques', 20),
            ('Consider therapy', 20)
        ]
        
        cursor.executemany("""
            INSERT INTO precautions (precaution_text, disease_id) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE precaution_text=precaution_text
        """, additional_precautions)
        print(f"✅ Added {len(additional_precautions)} more precautions")
        
        conn.commit()
        print("\n🎉 Database enhancement completed successfully!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM disease")
        disease_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user_accounts")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM medicines")
        medicine_count = cursor.fetchone()[0]
        
        print(f"\n📊 Current Database Status:")
        print(f"   - Diseases: {disease_count}")
        print(f"   - Users: {user_count}")
        print(f"   - Medicines: {medicine_count}")
        print(f"   - New Tables: 6 (consultations, users, relationships, treatment_plans, severity, etc.)")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    enhance_database()
