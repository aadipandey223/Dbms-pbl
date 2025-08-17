import mysql.connector
import re

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
        
        # Read the SQL file
        with open('Patient_entry.sql', 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split SQL commands by semicolon
        sql_commands = sql_content.split(';')
        
        print("📋 Setting up database...")
        
        for command in sql_commands:
            # Clean up the command
            command = command.strip()
            if command and not command.startswith('--') and not command.startswith('/*'):
                try:
                    cursor.execute(command)
                    print(f"✅ Executed: {command[:50]}...")
                except mysql.connector.Error as err:
                    if "database exists" not in str(err).lower():
                        print(f"⚠️ Warning: {err}")
        
        conn.commit()
        print("✅ Database setup completed!")
        
        # Now test the connection to the new database
        cursor.close()
        conn.close()
        
        # Test connection to the new database
        test_connection()
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="patient"
        )
        cursor = conn.cursor()
        
        print("\n🔍 Testing database connection...")
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check diseases
        cursor.execute("SELECT COUNT(*) FROM disease")
        disease_count = cursor.fetchone()[0]
        print(f"✅ Found {disease_count} diseases")
        
        # Check medicines
        cursor.execute("SELECT COUNT(*) FROM medicines")
        medicine_count = cursor.fetchone()[0]
        print(f"✅ Found {medicine_count} medicines")
        
        # Check precautions
        cursor.execute("SELECT COUNT(*) FROM precautions")
        precaution_count = cursor.fetchone()[0]
        print(f"✅ Found {precaution_count} precautions")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Database setup and testing completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ Test connection failed: {err}")

if __name__ == "__main__":
    setup_database()
