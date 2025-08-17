import mysql.connector
from typing import List, Dict, Tuple
import json

class DiagnosisEngine:
    def __init__(self, host="localhost", user="root", password="password", database="patient"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to the database"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Database connection error: {err}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def get_all_symptoms(self) -> List[str]:
        """Get all available symptoms from the database"""
        try:
            self.cursor.execute("SHOW COLUMNS FROM symptoms_table")
            columns = [row[0] for row in self.cursor.fetchall()]
            # Remove registration_id and return only symptom columns
            return [col for col in columns if col != 'registration_id']
        except Exception as e:
            print(f"❌ Error getting symptoms: {e}")
            return []
    
    def get_disease_symptoms(self, disease_id: int) -> List[str]:
        """Get all symptoms for a specific disease"""
        try:
            self.cursor.execute("""
                SELECT symptom_name FROM disease_symptom 
                WHERE disease_id = %s
            """, (disease_id,))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"❌ Error getting disease symptoms: {e}")
            return []
    
    def get_all_diseases(self) -> List[Dict]:
        """Get all diseases with their information"""
        try:
            self.cursor.execute("""
                SELECT disease_id, disease_name, description 
                FROM disease
            """)
            diseases = []
            for row in self.cursor.fetchall():
                diseases.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                })
            return diseases
        except Exception as e:
            print(f"❌ Error getting diseases: {e}")
            return []
    
    def analyze_symptoms(self, patient_symptoms: List[str]) -> List[Dict]:
        """
        Analyze patient symptoms and return ranked disease matches
        
        Args:
            patient_symptoms: List of symptom names the patient has
            
        Returns:
            List of dictionaries with disease info and match scores
        """
        if not self.connect():
            return []
        
        try:
            # Get all diseases
            diseases = self.get_all_diseases()
            disease_scores = []
            
            for disease in diseases:
                disease_id = disease['id']
                
                # Get all symptoms for this disease
                disease_symptoms = self.get_disease_symptoms(disease_id)
                
                if not disease_symptoms:
                    continue
                
                # Calculate match score
                matched_symptoms = []
                unmatched_symptoms = []
                
                for symptom in disease_symptoms:
                    if symptom in patient_symptoms:
                        matched_symptoms.append(symptom)
                    else:
                        unmatched_symptoms.append(symptom)
                
                # Calculate score based on:
                # 1. Percentage of disease symptoms that match patient symptoms
                # 2. Number of patient symptoms that match disease symptoms
                # 3. Weighted scoring system
                
                match_percentage = len(matched_symptoms) / len(disease_symptoms) * 100
                patient_match_percentage = len(matched_symptoms) / len(patient_symptoms) * 100
                
                # Weighted score (70% disease match, 30% patient match)
                weighted_score = (match_percentage * 0.7) + (patient_match_percentage * 0.3)
                
                # Get medicines and precautions for this disease
                medicines = self.get_disease_medicines(disease_id)
                precautions = self.get_disease_precautions(disease_id)
                
                disease_scores.append({
                    'disease': disease,
                    'matched_symptoms': matched_symptoms,
                    'unmatched_symptoms': unmatched_symptoms,
                    'match_percentage': round(match_percentage, 2),
                    'patient_match_percentage': round(patient_match_percentage, 2),
                    'weighted_score': round(weighted_score, 2),
                    'medicines': medicines,
                    'precautions': precautions
                })
            
            # Sort by weighted score (highest first)
            disease_scores.sort(key=lambda x: x['weighted_score'], reverse=True)
            
            return disease_scores
            
        except Exception as e:
            print(f"❌ Error analyzing symptoms: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_disease_medicines(self, disease_id: int) -> List[Dict]:
        """Get medicines for a specific disease"""
        try:
            self.cursor.execute("""
                SELECT medicine_name, dosage 
                FROM medicines 
                WHERE disease_id = %s
            """, (disease_id,))
            medicines = []
            for row in self.cursor.fetchall():
                medicines.append({
                    'name': row[0],
                    'dosage': row[1]
                })
            return medicines
        except Exception as e:
            print(f"❌ Error getting medicines: {e}")
            return []
    
    def get_disease_precautions(self, disease_id: int) -> List[str]:
        """Get precautions for a specific disease"""
        try:
            self.cursor.execute("""
                SELECT precaution_text 
                FROM precautions 
                WHERE disease_id = %s
            """, (disease_id,))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"❌ Error getting precautions: {e}")
            return []
    
    def get_symptom_suggestions(self, partial_symptom: str) -> List[str]:
        """Get symptom suggestions based on partial input"""
        if not self.connect():
            return []
        
        try:
            all_symptoms = self.get_all_symptoms()
            suggestions = []
            
            partial_lower = partial_symptom.lower()
            for symptom in all_symptoms:
                if partial_lower in symptom.lower():
                    suggestions.append(symptom)
            
            return suggestions[:10]  # Limit to 10 suggestions
            
        except Exception as e:
            print(f"❌ Error getting symptom suggestions: {e}")
            return []
        finally:
            self.disconnect()

def test_diagnosis_engine():
    """Test the diagnosis engine with sample symptoms"""
    engine = DiagnosisEngine()
    
    print("🧪 Testing Diagnosis Engine...")
    print("=" * 50)
    
    # Test 1: Get all symptoms
    print("📋 Available symptoms:")
    symptoms = engine.get_all_symptoms()
    print(f"Found {len(symptoms)} symptoms")
    print("Sample symptoms:", symptoms[:10])
    print()
    
    # Test 2: Get all diseases
    print("🦠 Available diseases:")
    diseases = engine.get_all_diseases()
    print(f"Found {len(diseases)} diseases")
    for disease in diseases[:3]:
        print(f"  - {disease['name']}: {disease['description']}")
    print()
    
    # Test 3: Test symptom analysis
    print("🔍 Testing symptom analysis...")
    test_symptoms = ['fever', 'dry_cough', 'fatigue', 'chest_pain']
    print(f"Patient symptoms: {test_symptoms}")
    
    results = engine.analyze_symptoms(test_symptoms)
    
    if results:
        print(f"\nTop 3 disease matches:")
        for i, result in enumerate(results[:3], 1):
            disease = result['disease']
            print(f"\n{i}. {disease['name']} (Score: {result['weighted_score']}%)")
            print(f"   Description: {disease['description']}")
            print(f"   Matched symptoms: {', '.join(result['matched_symptoms'])}")
            print(f"   Match percentage: {result['match_percentage']}%")
            
            if result['medicines']:
                print(f"   Medicines:")
                for med in result['medicines']:
                    print(f"     - {med['name']}: {med['dosage']}")
            
            if result['precautions']:
                print(f"   Precautions:")
                for precaution in result['precautions'][:3]:  # Show first 3
                    print(f"     - {precaution}")
    else:
        print("❌ No diagnosis results found")
    
    print("\n" + "=" * 50)
    print("✅ Diagnosis engine test completed!")

if __name__ == "__main__":
    test_diagnosis_engine()
