# 🏥 MediCare Hospital System - Startup Guide

## 🚨 Problem Solved
Your web page wasn't loading because:
1. The database was being dropped by `delsql.py`
2. The backend server wasn't running
3. Missing database setup

## 🚀 Quick Start (Recommended)

### Option 1: Automatic Setup (Easiest)
```bash
python start_server.py
```
This will:
- ✅ Check dependencies
- ✅ Setup database automatically
- ✅ Start the backend server
- ✅ Open http://localhost:5001

### Option 2: Manual Setup
```bash
# 1. Setup database
python setup_database.py

# 2. Start backend server
python enhanced_api.py

# 3. In another terminal, start frontend
python serve_frontend.py
```

## 📋 Prerequisites

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. MySQL Server
Make sure MySQL is running with:
- Host: localhost
- User: root
- Password: password

## 🔐 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Doctor | doctor | doctor123 |
| Nurse | nurse | nurse123 |

## 🌐 Access URLs

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/api/health

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check if MySQL is running
mysql -u root -p

# If password is different, update DB_CONFIG in enhanced_api.py
```

### Port Already in Use
```bash
# Kill process on port 5001
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Or change port in enhanced_api.py
```

### Missing Dependencies
```bash
pip install flask flask-cors mysql-connector-python
```

## 📁 File Structure
```
Dbms-pbl/
├── enhanced_api.py          # Backend server
├── start_server.py          # Automatic startup
├── setup_database.py        # Database setup
├── serve_frontend.py        # Frontend server
├── index.html              # Main web page
├── app.js                  # Frontend JavaScript
├── style.css               # Styling
├── Patient_entry.sql       # Database schema
└── requirements.txt        # Python dependencies
```

## 🎯 Features Available

### For Patients:
- ✅ Patient registration
- ✅ Symptom analysis with AI
- ✅ Disease diagnosis
- ✅ Treatment recommendations

### For Medical Staff:
- ✅ User authentication
- ✅ Patient management
- ✅ Consultation history
- ✅ Analytics dashboard

## 🆘 Need Help?

1. Check the console output for error messages
2. Verify MySQL is running
3. Ensure all dependencies are installed
4. Check if ports 5000 and 5001 are available

## 🔄 Reset Everything

If you need to start fresh:
```bash
# 1. Stop all servers (Ctrl+C)
# 2. Run database setup again
python setup_database.py
# 3. Start the system
python start_server.py
```
