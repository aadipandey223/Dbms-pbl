import subprocess
import sys
import time
import os
from setup_database import setup_database

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'flask_cors', 'mysql.connector']
    
    print("🔍 Checking dependencies...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            print(f"   Install with: pip install {package.replace('.', '-')}")
            return False
    return True

def start_server():
    """Start the enhanced API server"""
    print("🚀 Starting Enhanced Patient Diagnosis System...")
    
    # Check dependencies first
    if not check_dependencies():
        print("❌ Please install missing dependencies and try again")
        return False
    
    # Setup database
    print("\n🔧 Setting up database...")
    if not setup_database():
        print("❌ Database setup failed")
        return False
    
    # Start the server
    print("\n🌐 Starting server on http://localhost:8000")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("🔐 Login credentials:")
    print("   - Admin: admin/admin123")
    print("   - Doctor: doctor/doctor123")
    print("   - Nurse: nurse/nurse123")
    print("\n" + "="*60)
    
    try:
        # Start the Flask server
        subprocess.run([sys.executable, 'enhanced_api.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_server()
