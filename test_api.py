import requests
import json

# API base URL
API_BASE = 'http://localhost:5000/api'

def test_api():
    print("🧪 Testing Patient Diagnosis System API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']} - {data['service']} v{data['version']}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")
    
    print()
    
    # Test 2: Get Symptoms
    print("2. Testing Symptoms API...")
    try:
        response = requests.get(f"{API_BASE}/symptoms")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Symptoms API: Found {data['count']} symptoms")
            print(f"   Sample symptoms: {', '.join(data['symptoms'][:5])}")
        else:
            print(f"❌ Symptoms API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Symptoms API error: {e}")
    
    print()
    
    # Test 3: Get Diseases
    print("3. Testing Diseases API...")
    try:
        response = requests.get(f"{API_BASE}/diseases")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Diseases API: Found {data['count']} diseases")
            for disease in data['diseases'][:3]:
                print(f"   - {disease['name']}: {disease['description']}")
        else:
            print(f"❌ Diseases API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Diseases API error: {e}")
    
    print()
    
    # Test 4: Symptom Suggestions
    print("4. Testing Symptom Suggestions...")
    try:
        response = requests.get(f"{API_BASE}/symptoms/suggest?q=fever")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Symptom Suggestions: Found {len(data['suggestions'])} suggestions for 'fever'")
            print(f"   Suggestions: {', '.join(data['suggestions'])}")
        else:
            print(f"❌ Symptom Suggestions failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Symptom Suggestions error: {e}")
    
    print()
    
    # Test 5: Diagnosis API
    print("5. Testing Diagnosis API...")
    test_symptoms = ["fever", "dry_cough", "fatigue", "chest_pain"]
    try:
        response = requests.post(f"{API_BASE}/diagnose", 
                               json={"symptoms": test_symptoms},
                               headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Diagnosis API: Found {data['total_matches']} disease matches")
            print(f"   Symptoms analyzed: {', '.join(data['symptoms_analyzed'])}")
            
            if data['diagnosis']:
                top_result = data['diagnosis'][0]
                disease = top_result['disease']
                print(f"   Top match: {disease['name']} (Score: {top_result['weighted_score']}%)")
                print(f"   Matched symptoms: {', '.join(top_result['matched_symptoms'])}")
                
                if top_result['medicines']:
                    print(f"   Medicines: {len(top_result['medicines'])} available")
                
                if top_result['precautions']:
                    print(f"   Precautions: {len(top_result['precautions'])} available")
        else:
            print(f"❌ Diagnosis API failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Diagnosis API error: {e}")
    
    print()
    
    # Test 6: Patient Registration
    print("6. Testing Patient Registration...")
    test_patient = {
        "name": "John Doe",
        "gender": "Male",
        "age": 30,
        "contact": "1234567890"
    }
    try:
        response = requests.post(f"{API_BASE}/patient/register", 
                               json=test_patient,
                               headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Patient Registration: Successfully registered patient")
            print(f"   Registration ID: {data['registration_id']}")
            print(f"   Message: {data['message']}")
            
            # Store registration ID for symptom recording test
            patient_id = data['registration_id']
            
            # Test 7: Record Patient Symptoms
            print("\n7. Testing Symptom Recording...")
            test_symptoms = ["fever", "headache"]
            try:
                symptom_response = requests.post(f"{API_BASE}/patient/{patient_id}/symptoms", 
                                              json={"symptoms": test_symptoms},
                                              headers={"Content-Type": "application/json"})
                if symptom_response.status_code == 200:
                    symptom_data = symptom_response.json()
                    print(f"✅ Symptom Recording: Successfully recorded symptoms")
                    print(f"   Symptoms recorded: {', '.join(symptom_data['symptoms_recorded'])}")
                else:
                    print(f"❌ Symptom Recording failed: {symptom_response.status_code}")
            except Exception as e:
                print(f"❌ Symptom Recording error: {e}")
                
        else:
            print(f"❌ Patient Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Patient Registration error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Completed!")
    print("\n📱 Now test the web interface:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Click 'Symptom Analysis'")
    print("   3. Register a patient and test the diagnosis!")

if __name__ == "__main__":
    test_api()
