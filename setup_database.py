import mysql.connector
import os

def setup_database():
    """Setup the patient database with all required tables and data"""
    
    # Database configuration
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password'
    }
    
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔧 Setting up database...")
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS patient")
        cursor.execute("USE patient")
        
        print("✅ Database 'patient' created/verified")
        
        # Read and execute the SQL file
        with open('Patient_entry.sql', 'r') as file:
            sql_content = file.read()
        
        # Split by semicolon and execute each statement
        statements = sql_content.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    print(f"✅ Executed: {statement[:50]}...")
                except mysql.connector.Error as err:
                    if "already exists" not in str(err).lower():
                        print(f"⚠️  Warning: {err}")
        
        # Create additional tables for enhanced features
        print("🔧 Creating enhanced feature tables...")
        
        # User accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_accounts (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                role ENUM('admin', 'doctor', 'nurse', 'patient') DEFAULT 'patient',
                full_name VARCHAR(100),
                specialization VARCHAR(100),
                license_number VARCHAR(50),
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Consultations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                consultation_id INT PRIMARY KEY AUTO_INCREMENT,
                patient_id VARCHAR(10),
                symptoms_analyzed JSON,
                diagnosis_results JSON,
                confidence_score DECIMAL(5,4),
                doctor_notes TEXT,
                follow_up_date DATE,
                status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
                consultation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patient_table(registration_id)
            )
        """)
        
        # Treatment plans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treatment_plans (
                plan_id INT PRIMARY KEY AUTO_INCREMENT,
                consultation_id INT,
                disease_id INT,
                treatment_description TEXT,
                created_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id),
                FOREIGN KEY (disease_id) REFERENCES disease(disease_id),
                FOREIGN KEY (created_by) REFERENCES user_accounts(user_id)
            )
        """)
        
        # Insert default admin user
        cursor.execute("""
            INSERT IGNORE INTO user_accounts (username, password_hash, role, full_name, email)
            VALUES ('admin', 'admin123', 'admin', 'System Administrator', 'admin@hospital.com')
        """)
        
        # Insert sample doctor
        cursor.execute("""
            INSERT IGNORE INTO user_accounts (username, password_hash, role, full_name, specialization, license_number, email)
            VALUES ('doctor', 'doctor123', 'doctor', 'Dr. John Smith', 'General Medicine', 'MD12345', 'doctor@hospital.com')
        """)
        
        # Insert sample nurse
        cursor.execute("""
            INSERT IGNORE INTO user_accounts (username, password_hash, role, full_name, specialization, email)
            VALUES ('nurse', 'nurse123', 'nurse', 'Nurse Sarah Johnson', 'Emergency Care', 'nurse@hospital.com')
        """)
        
        conn.commit()
        print("✅ Enhanced tables created successfully")
        print("✅ Default users created:")
        print("   - Admin: admin/admin123")
        print("   - Doctor: doctor/doctor123")
        print("   - Nurse: nurse/nurse123")
        
        cursor.close()
        conn.close()
        
        print("🎉 Database setup completed successfully!")
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Database setup failed: {err}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    setup_database()
