from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import mysql.connector
import json
from datetime import datetime, date
import hashlib
from functools import wraps

app = Flask(__name__)
app.secret_key = 'medicare_secret_key_2025'
CORS(app, supports_credentials=True)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'patient'
}

def get_db_connection():
    """Get database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Authentication middleware
def require_auth(required_role=None):
    """Decorator to require authentication"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            
            if required_role:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT role FROM user_accounts WHERE user_id = %s", (session['user_id'],))
                    user_role = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if not user_role or user_role[0] not in required_role:
                        return jsonify({'success': False, 'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# User Authentication Endpoints
@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Simple password check (in production, use proper hashing)
        cursor.execute("""
            SELECT user_id, username, role, full_name, specialization, license_number 
            FROM user_accounts 
            WHERE username = %s AND password_hash = %s AND is_active = 1
        """, (username, password))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[2]
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user[0],
                    'username': user[1],
                    'role': user[2],
                    'full_name': user[3],
                    'specialization': user[4],
                    'license_number': user[5]
                },
                'message': 'Login successful'
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    """User logout endpoint"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful'})

@app.route('/api/auth/profile', methods=['GET'])
@require_auth()
def auth_profile():
    """Get current user profile"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, username, email, role, full_name, specialization, license_number, created_at
            FROM user_accounts 
            WHERE user_id = %s
        """, (session['user_id'],))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'role': user[3],
                    'full_name': user[4],
                    'specialization': user[5],
                    'license_number': user[6],
                    'created_at': user[7].isoformat() if user[7] else None
                }
            })
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Basic API endpoints (for existing frontend compatibility)
@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT symptom_name FROM disease_symptom ORDER BY symptom_name")
        symptoms = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'symptoms': symptoms,
            'count': len(symptoms)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/symptoms/suggest', methods=['GET'])
def suggest_symptoms():
    """Get symptom suggestions based on query"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'success': False, 'error': 'Query parameter required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT symptom_name FROM disease_symptom WHERE symptom_name LIKE %s ORDER BY symptom_name", (f'%{query}%',))
        suggestions = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get all diseases"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT disease_id, disease_name, description FROM disease ORDER BY disease_name")
        diseases = []
        for row in cursor.fetchall():
            diseases.append({
                'id': row[0],
                'name': row[1],
                'description': row[2]
            })
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'diseases': diseases,
            'count': len(diseases)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patient/register', methods=['POST'])
def register_patient():
    """Register a new patient"""
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        contact = data.get('contact')
        
        print(f"DEBUG: Received data - name: {name}, age: {age}, gender: {gender}, contact: {contact}")
        
        if not all([name, age, gender, contact]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Generate registration ID
        import random
        import string
        registration_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        print(f"DEBUG: Generated registration_id: {registration_id}")
        
        # Insert patient
        cursor.execute("""
            INSERT INTO patient_table (registration_id, name, gender, age, contact)
            VALUES (%s, %s, %s, %s, %s)
        """, (registration_id, name, gender, age, contact))
        
        print("DEBUG: Patient inserted successfully")
        
        # Initialize symptoms table entry with all symptoms set to false
        cursor.execute("""
            INSERT INTO symptoms_table (registration_id) VALUES (%s)
        """, (registration_id,))
        
        print("DEBUG: Symptoms table entry created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'registration_id': registration_id,
            'message': 'Patient registered successfully'
        })
        
    except Exception as e:
        print(f"DEBUG: Error in register_patient: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/diagnose', methods=['POST'])
def diagnose_symptoms():
    """Diagnose symptoms and return disease matches"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        patient_id = data.get('patient_id')
        
        print(f"DEBUG: Diagnosis request - symptoms: {symptoms}, patient_id: {patient_id}")
        
        if not symptoms:
            return jsonify({'success': False, 'error': 'Symptoms are required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get all diseases and their symptoms
        cursor.execute("""
            SELECT d.disease_id, d.disease_name, d.description, ds.symptom_name
            FROM disease d
            JOIN disease_symptom ds ON d.disease_id = ds.disease_id
        """)
        
        disease_symptoms = {}
        for row in cursor.fetchall():
            disease_id, disease_name, description, symptom = row
            if disease_id not in disease_symptoms:
                disease_symptoms[disease_id] = {
                    'id': disease_id,
                    'name': disease_name,
                    'description': description,
                    'symptoms': [],
                    'matched_symptoms': [],
                    'medicines': [],
                    'precautions': []
                }
            disease_symptoms[disease_id]['symptoms'].append(symptom)
        
        # Analyze symptoms for each disease
        results = []
        for disease_id, disease_data in disease_symptoms.items():
            matched_symptoms = [s for s in symptoms if s in disease_data['symptoms']]
            if matched_symptoms:
                match_percentage = (len(matched_symptoms) / len(disease_data['symptoms'])) * 100
                patient_match_percentage = (len(matched_symptoms) / len(symptoms)) * 100
                weighted_score = (match_percentage * 0.7) + (patient_match_percentage * 0.3)
                
                # Get medicines for this disease
                cursor.execute("SELECT medicine_name, dosage FROM medicines WHERE disease_id = %s", (disease_id,))
                medicines = [{'name': row[0], 'dosage': row[1]} for row in cursor.fetchall()]
                
                # Get precautions for this disease
                cursor.execute("SELECT precaution_text FROM precautions WHERE disease_id = %s", (disease_id,))
                precautions = [row[0] for row in cursor.fetchall()]
                
                disease_data['matched_symptoms'] = matched_symptoms
                disease_data['medicines'] = medicines
                disease_data['precautions'] = precautions
                disease_data['confidence'] = weighted_score / 100
                
                results.append({
                    'disease': disease_data,
                    'match_percentage': match_percentage,
                    'patient_match_percentage': patient_match_percentage,
                    'weighted_score': weighted_score
                })
        
        # Sort by weighted score
        results.sort(key=lambda x: x['weighted_score'], reverse=True)
        
        # Update symptoms table if patient_id provided
        if patient_id:
            # First, reset all symptoms to false
            cursor.execute("""
                UPDATE symptoms_table 
                SET fever = 0, high_fever = 0, mild_fever = 0, chills = 0, fatigue = 0,
                    weakness = 0, body_ache = 0, body_pain = 0, night_sweats = 0, sweating = 0,
                    weight_loss = 0, dry_cough = 0, wet_cough = 0, persistent_cough = 0,
                    blood_in_cough = 0, chest_pain = 0, chest_tightness = 0, breathing_difficulty = 0,
                    fast_breathing = 0, sore_throat = 0, runny_nose = 0, sneezing = 0,
                    nasal_congestion = 0, nausea = 0, vomiting = 0, diarrhea = 0, constipation = 0,
                    stomach_pain = 0, stomach_cramps = 0, loss_of_appetite = 0, appetite_loss = 0,
                    dehydration = 0, dizziness = 0, headache = 0, confusion = 0, rash = 0,
                    skin_rash = 0, skin_blisters = 0, red_eyes = 0, watery_eyes = 0, itchy_eyes = 0,
                    itchy_throat = 0, eye_pain = 0, ear_pain = 0, bleeding_gums = 0, low_platelet = 0,
                    difficulty_swallowing = 0, swollen_tonsils = 0, white_spots_mouth = 0
                WHERE registration_id = %s
            """, (patient_id,))
            
            # Then set the specific symptoms to true
            for symptom in symptoms:
                if symptom in ['fever', 'high_fever', 'mild_fever', 'chills', 'fatigue', 'weakness', 
                              'body_ache', 'body_pain', 'night_sweats', 'sweating', 'weight_loss',
                              'dry_cough', 'wet_cough', 'persistent_cough', 'blood_in_cough',
                              'chest_pain', 'chest_tightness', 'breathing_difficulty', 'fast_breathing',
                              'sore_throat', 'runny_nose', 'sneezing', 'nasal_congestion', 'nausea',
                              'vomiting', 'diarrhea', 'constipation', 'stomach_pain', 'stomach_cramps',
                              'loss_of_appetite', 'appetite_loss', 'dehydration', 'dizziness',
                              'headache', 'confusion', 'rash', 'skin_rash', 'skin_blisters',
                              'red_eyes', 'watery_eyes', 'itchy_eyes', 'itchy_throat', 'eye_pain',
                              'ear_pain', 'bleeding_gums', 'low_platelet', 'difficulty_swallowing',
                              'swollen_tonsils', 'white_spots_mouth']:
                    cursor.execute(f"""
                        UPDATE symptoms_table 
                        SET {symptom} = 1 
                        WHERE registration_id = %s
                    """, (patient_id,))
            
            conn.commit()
        
        cursor.close()
        conn.close()
        
        print(f"DEBUG: Diagnosis completed - found {len(results)} matching diseases")
        
        return jsonify({
            'success': True,
            'results': results,
            'top_disease': results[0]['disease'] if results else None
        })
        
    except Exception as e:
        print(f"DEBUG: Error in diagnose_symptoms: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Consultation Management Endpoints
@app.route('/api/consultations', methods=['POST'])
@require_auth(['doctor', 'nurse', 'admin'])
def create_consultation():
    """Create a new consultation"""
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        symptoms = data.get('symptoms', [])
        diagnosis_results = data.get('diagnosis_results', {})
        confidence_score = data.get('confidence_score', 0.0)
        doctor_notes = data.get('doctor_notes', '')
        follow_up_date = data.get('follow_up_date')
        
        if not patient_id:
            return jsonify({'success': False, 'error': 'Patient ID required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Create consultation
        cursor.execute("""
            INSERT INTO consultations (patient_id, symptoms_analyzed, diagnosis_results, confidence_score, doctor_notes, follow_up_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            patient_id,
            json.dumps(symptoms),
            json.dumps(diagnosis_results),
            confidence_score,
            doctor_notes,
            follow_up_date
        ))
        
        consultation_id = cursor.lastrowid
        
        # Create treatment plan if diagnosis exists
        if diagnosis_results and 'top_disease' in diagnosis_results:
            disease_id = diagnosis_results['top_disease'].get('id')
            if disease_id:
                cursor.execute("""
                    INSERT INTO treatment_plans (consultation_id, disease_id, treatment_description, created_by)
                    VALUES (%s, %s, %s, %s)
                """, (
                    consultation_id,
                    disease_id,
                    f"Treatment plan for {diagnosis_results['top_disease'].get('name', 'diagnosed condition')}",
                    session['user_id']
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'consultation_id': consultation_id,
            'message': 'Consultation created successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultations/<patient_id>', methods=['GET'])
@require_auth(['doctor', 'nurse', 'admin'])
def get_patient_consultations(patient_id):
    """Get consultation history for a patient"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.consultation_id, c.consultation_date, c.symptoms_analyzed, c.diagnosis_results,
                   c.confidence_score, c.doctor_notes, c.follow_up_date, c.status,
                   u.full_name as doctor_name
            FROM consultations c
            LEFT JOIN user_accounts u ON c.doctor_notes LIKE CONCAT('%', u.full_name, '%')
            WHERE c.patient_id = %s
            ORDER BY c.consultation_date DESC
        """, (patient_id,))
        
        consultations = []
        for row in cursor.fetchall():
            consultations.append({
                'consultation_id': row[0],
                'consultation_date': row[1].isoformat() if row[1] else None,
                'symptoms_analyzed': json.loads(row[2]) if row[2] else [],
                'diagnosis_results': json.loads(row[3]) if row[3] else {},
                'confidence_score': float(row[4]) if row[4] else 0.0,
                'doctor_notes': row[5],
                'follow_up_date': row[6].isoformat() if row[6] else None,
                'status': row[7],
                'doctor_name': row[8] or 'System'
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'consultations': consultations,
            'count': len(consultations)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Patient Management Endpoints
@app.route('/api/patients', methods=['GET'])
@require_auth(['doctor', 'nurse', 'admin'])
def get_all_patients():
    """Get all patients (for doctors/nurses)"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.registration_id, p.name, p.gender, p.age, p.contact,
                   COUNT(c.consultation_id) as consultation_count,
                   MAX(c.consultation_date) as last_visit
            FROM patient_table p
            LEFT JOIN consultations c ON p.registration_id = c.patient_id
            GROUP BY p.registration_id
            ORDER BY p.name
        """)
        
        patients = []
        for row in cursor.fetchall():
            patients.append({
                'registration_id': row[0],
                'name': row[1],
                'gender': row[2],
                'age': row[3],
                'contact': row[4],
                'consultation_count': row[5],
                'last_visit': row[6].isoformat() if row[6] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'patients': patients,
            'count': len(patients)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients/<patient_id>/summary', methods=['GET'])
@require_auth(['doctor', 'nurse', 'admin'])
def get_patient_summary(patient_id):
    """Get comprehensive patient summary"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get patient info
        cursor.execute("SELECT * FROM patient_table WHERE registration_id = %s", (patient_id,))
        patient = cursor.fetchone()
        
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404
        
        # Get consultation history
        cursor.execute("""
            SELECT consultation_date, symptoms_analyzed, diagnosis_results, confidence_score, status
            FROM consultations 
            WHERE patient_id = %s 
            ORDER BY consultation_date DESC
        """, (patient_id,))
        
        consultations = []
        for row in cursor.fetchall():
            consultations.append({
                'date': row[0].isoformat() if row[0] else None,
                'symptoms': json.loads(row[1]) if row[1] else [],
                'diagnosis': json.loads(row[2]) if row[2] else {},
                'confidence': float(row[3]) if row[3] else 0.0,
                'status': row[4]
            })
        
        # Get symptoms history
        cursor.execute("SELECT * FROM symptoms_table WHERE registration_id = %s", (patient_id,))
        symptoms = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'patient': {
                'registration_id': patient[0],
                'name': patient[1],
                'gender': patient[2],
                'age': patient[3],
                'contact': patient[4]
            },
            'consultations': consultations,
            'symptoms_history': symptoms[1:] if symptoms else [],  # Skip registration_id
            'total_consultations': len(consultations)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytics Endpoints
@app.route('/api/analytics/dashboard', methods=['GET'])
@require_auth(['admin', 'doctor'])
def get_dashboard_analytics():
    """Get dashboard analytics"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Total patients
        cursor.execute("SELECT COUNT(*) FROM patient_table")
        total_patients = cursor.fetchone()[0]
        
        # Total consultations today
        cursor.execute("SELECT COUNT(*) FROM consultations WHERE DATE(consultation_date) = CURDATE()")
        today_consultations = cursor.fetchone()[0]
        
        # Total consultations this month
        cursor.execute("SELECT COUNT(*) FROM consultations WHERE MONTH(consultation_date) = MONTH(CURDATE())")
        month_consultations = cursor.fetchone()[0]
        
        # Most common diseases
        cursor.execute("""
            SELECT d.disease_name, COUNT(*) as frequency
            FROM consultations c
            JOIN JSON_TABLE(c.diagnosis_results, '$[*].disease.id' COLUMNS (disease_id INT PATH '$')) as jt
            JOIN disease d ON jt.disease_id = d.disease_id
            GROUP BY d.disease_id, d.disease_name
            ORDER BY frequency DESC
            LIMIT 5
        """)
        
        common_diseases = []
        for row in cursor.fetchall():
            common_diseases.append({
                'disease': row[0],
                'frequency': row[1]
            })
        
        # Recent consultations
        cursor.execute("""
            SELECT c.consultation_date, p.name, c.confidence_score, c.status
            FROM consultations c
            JOIN patient_table p ON c.patient_id = p.registration_id
            ORDER BY c.consultation_date DESC
            LIMIT 10
        """)
        
        recent_consultations = []
        for row in cursor.fetchall():
            recent_consultations.append({
                'date': row[0].isoformat() if row[0] else None,
                'patient_name': row[1],
                'confidence': float(row[2]) if row[2] else 0.0,
                'status': row[3]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'analytics': {
                'total_patients': total_patients,
                'today_consultations': today_consultations,
                'month_consultations': month_consultations,
                'common_diseases': common_diseases,
                'recent_consultations': recent_consultations
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Get table counts
            cursor.execute("SELECT COUNT(*) FROM disease")
            disease_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_accounts")
            user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM consultations")
            consultation_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'status': 'healthy',
                'service': 'Enhanced Patient Diagnosis System',
                'version': '2.0.0',
                'database': {
                    'diseases': disease_count,
                    'users': user_count,
                    'consultations': consultation_count
                },
                'features': [
                    'AI-Powered Diagnosis',
                    'Patient History Tracking',
                    'User Authentication',
                    'Consultation Management',
                    'Analytics Dashboard'
                ]
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'error': 'Database connection failed'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    print("🚀 Starting Enhanced Patient Diagnosis System...")
    print("📱 Enhanced API will be available at: http://localhost:8000")
    print("🔐 New Features:")
    print("   - User Authentication & Role Management")
    print("   - Patient Consultation History")
    print("   - Treatment Plan Management")
    print("   - Analytics Dashboard")
    print("   - Patient-Doctor Relationships")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=8000)
