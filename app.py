from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from diagnosis_engine import DiagnosisEngine
import mysql.connector
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize diagnosis engine
diagnosis_engine = DiagnosisEngine()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template_string(open('index.html').read())

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms"""
    try:
        engine = DiagnosisEngine()
        if engine.connect():
            symptoms = engine.get_all_symptoms()
            engine.disconnect()
            return jsonify({
                'success': True,
                'symptoms': symptoms,
                'count': len(symptoms)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/symptoms/suggest', methods=['GET'])
def suggest_symptoms():
    """Get symptom suggestions based on partial input"""
    try:
        partial = request.args.get('q', '')
        if not partial:
            return jsonify({
                'success': False,
                'error': 'Query parameter "q" is required'
            }), 400
        
        engine = DiagnosisEngine()
        if engine.connect():
            suggestions = engine.get_symptom_suggestions(partial)
            engine.disconnect()
            return jsonify({
                'success': True,
                'suggestions': suggestions,
                'query': partial
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """Analyze symptoms and provide diagnosis"""
    try:
        data = request.get_json()
        if not data or 'symptoms' not in data:
            return jsonify({
                'success': False,
                'error': 'Symptoms list is required'
            }), 400
        
        symptoms = data['symptoms']
        if not isinstance(symptoms, list) or len(symptoms) == 0:
            return jsonify({
                'success': False,
                'error': 'Symptoms must be a non-empty list'
            }), 400
        
        # Get diagnosis results
        engine = DiagnosisEngine()
        if engine.connect():
            results = engine.analyze_symptoms(symptoms)
            engine.disconnect()
            
            if results:
                return jsonify({
                    'success': True,
                    'diagnosis': results,
                    'symptoms_analyzed': symptoms,
                    'total_matches': len(results)
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No disease matches found for the given symptoms'
                }), 404
        else:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/patient/register', methods=['POST'])
def register_patient():
    """Register a new patient"""
    try:
        data = request.get_json()
        required_fields = ['name', 'gender', 'age', 'contact']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Connect to database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="patient"
        )
        cursor = conn.cursor()
        
        # Generate registration ID
        cursor.execute("SELECT registration_id FROM patient_table ORDER BY registration_id DESC LIMIT 1")
        reg_id = cursor.fetchone()
        
        if reg_id is None:
            new_reg_id = "REG001"
        else:
            last_id_num = int(reg_id[0][3:])
            new_reg_id = f"REG{last_id_num + 1:03d}"
        
        # Insert patient data
        cursor.execute("""
            INSERT INTO patient_table (registration_id, name, gender, age, contact) 
            VALUES (%s, %s, %s, %s, %s)
        """, (new_reg_id, data['name'], data['gender'], data['age'], data['contact']))
        
        # Initialize symptoms row
        cursor.execute("INSERT INTO symptoms_table (registration_id) VALUES (%s)", (new_reg_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'registration_id': new_reg_id,
            'message': 'Patient registered successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/patient/<registration_id>/symptoms', methods=['POST'])
def record_patient_symptoms(registration_id):
    """Record symptoms for a specific patient"""
    try:
        data = request.get_json()
        if not data or 'symptoms' not in data:
            return jsonify({
                'success': False,
                'error': 'Symptoms list is required'
            }), 400
        
        symptoms = data['symptoms']
        
        # Connect to database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="patient"
        )
        cursor = conn.cursor()
        
        # Check if patient exists
        cursor.execute("SELECT registration_id FROM patient_table WHERE registration_id = %s", (registration_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Patient not found'
            }), 404
        
        # Update symptoms
        for symptom in symptoms:
            cursor.execute(f"UPDATE symptoms_table SET {symptom} = 1 WHERE registration_id = %s", (registration_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Symptoms recorded for patient {registration_id}',
            'symptoms_recorded': symptoms
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get all diseases"""
    try:
        engine = DiagnosisEngine()
        if engine.connect():
            diseases = engine.get_all_diseases()
            engine.disconnect()
            return jsonify({
                'success': True,
                'diseases': diseases,
                'count': len(diseases)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Patient Diagnosis System',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting Patient Diagnosis System...")
    print("📱 Web API will be available at: http://localhost:5000")
    print("🔍 Test the API endpoints:")
    print("   - GET  /api/health")
    print("   - GET  /api/symptoms")
    print("   - GET  /api/diseases")
    print("   - POST /api/diagnose")
    print("   - POST /api/patient/register")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
