CREATE DATABASE patient;
USE patient;

CREATE TABLE patient_table (
    registration_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    contact VARCHAR(15)
);

CREATE TABLE symptoms_table (
    registration_id VARCHAR(20) PRIMARY KEY,

    -- General
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

    -- Respiratory
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

    -- Gastrointestinal
    nausea BOOLEAN DEFAULT 0,
    vomiting BOOLEAN DEFAULT 0,
    diarrhea BOOLEAN DEFAULT 0,
    constipation BOOLEAN DEFAULT 0,
    stomach_pain BOOLEAN DEFAULT 0,
    stomach_cramps BOOLEAN DEFAULT 0,
    loss_of_appetite BOOLEAN DEFAULT 0,
    appetite_loss BOOLEAN DEFAULT 0,
    dehydration BOOLEAN DEFAULT 0,

    -- Neurological
    dizziness BOOLEAN DEFAULT 0,
    headache BOOLEAN DEFAULT 0,
    confusion BOOLEAN DEFAULT 0,

    -- Skin
    rash BOOLEAN DEFAULT 0,
    skin_rash BOOLEAN DEFAULT 0,
    skin_blisters BOOLEAN DEFAULT 0,
    red_eyes BOOLEAN DEFAULT 0,
    watery_eyes BOOLEAN DEFAULT 0,
    itchy_eyes BOOLEAN DEFAULT 0,
    itchy_throat BOOLEAN DEFAULT 0,

    -- Other
    eye_pain BOOLEAN DEFAULT 0,
    ear_pain BOOLEAN DEFAULT 0,
    bleeding_gums BOOLEAN DEFAULT 0,
    low_platelet BOOLEAN DEFAULT 0,
    difficulty_swallowing BOOLEAN DEFAULT 0,
    swollen_tonsils BOOLEAN DEFAULT 0,
    white_spots_mouth BOOLEAN DEFAULT 0,

    FOREIGN KEY (registration_id) REFERENCES patient_table(registration_id)
);

CREATE TABLE disease (
    disease_id INT PRIMARY KEY AUTO_INCREMENT,
    disease_name VARCHAR(100),
    description TEXT
);

CREATE TABLE disease_symptom (
    disease_id INT,
    symptom_name VARCHAR(50),
    FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
);

CREATE TABLE medicines (
    medicine_id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_name VARCHAR(100),
    dosage VARCHAR(100),
    disease_id INT,
    FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
);

CREATE TABLE precautions (
    precaution_id INT PRIMARY KEY AUTO_INCREMENT,
    precaution_text TEXT,
    disease_id INT,
    FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
);

-- Insert sample diseases
INSERT INTO disease (disease_name, description) VALUES
('Pneumonia', 'Infection that inflames air sacs in lungs'),
('COVID-19', 'Respiratory illness caused by coronavirus'),
('Dengue Fever', 'Viral infection transmitted by mosquitoes'),
('Common Cold', 'Viral upper respiratory tract infection'),
('Bronchial Asthma', 'Chronic respiratory condition with airway inflammation'),
('Gastroenteritis', 'Inflammation of stomach and intestines'),
('Migraine', 'Severe recurring headache'),
('Conjunctivitis', 'Inflammation of the eye conjunctiva'),
('Tonsillitis', 'Inflammation of tonsils'),
('Urinary Tract Infection', 'Infection in urinary system');

-- Insert disease-symptom mappings
INSERT INTO disease_symptom (disease_id, symptom_name) VALUES
-- Pneumonia
(1, 'fever'), (1, 'high_fever'), (1, 'dry_cough'), (1, 'chest_pain'), 
(1, 'breathing_difficulty'), (1, 'fatigue'), (1, 'chills'), (1, 'sweating'),

-- COVID-19
(2, 'fever'), (2, 'dry_cough'), (2, 'fatigue'), (2, 'body_ache'),
(2, 'sore_throat'), (2, 'headache'), (2, 'loss_of_appetite'), (2, 'diarrhea'),

-- Dengue Fever
(3, 'high_fever'), (3, 'headache'), (3, 'body_pain'), (3, 'rash'),
(3, 'low_platelet'), (3, 'nausea'), (3, 'vomiting'), (3, 'fatigue'),

-- Common Cold
(4, 'mild_fever'), (4, 'runny_nose'), (4, 'sneezing'), (4, 'sore_throat'),
(4, 'cough'), (4, 'nasal_congestion'), (4, 'fatigue'),

-- Bronchial Asthma
(5, 'breathing_difficulty'), (5, 'chest_tightness'), (5, 'persistent_cough'),
(5, 'wheezing'), (5, 'fatigue'),

-- Gastroenteritis
(6, 'nausea'), (6, 'vomiting'), (6, 'diarrhea'), (6, 'stomach_pain'),
(6, 'loss_of_appetite'), (6, 'dehydration'), (6, 'fever'),

-- Migraine
(7, 'headache'), (7, 'nausea'), (7, 'dizziness'), (7, 'sensitivity_to_light'),

-- Conjunctivitis
(8, 'red_eyes'), (8, 'watery_eyes'), (8, 'itchy_eyes'), (8, 'eye_pain'),

-- Tonsillitis
(9, 'sore_throat'), (9, 'difficulty_swallowing'), (9, 'swollen_tonsils'),
(9, 'fever'), (9, 'headache'), (9, 'white_spots_mouth'),

-- UTI
(10, 'frequent_urination'), (10, 'burning_sensation'), (10, 'fever'), (10, 'nausea');

-- Insert sample medicines
INSERT INTO medicines (medicine_name, dosage, disease_id) VALUES
-- Pneumonia
('Azithromycin', '500mg once daily for 3-5 days', 1),
('Amoxicillin', '500mg three times daily for 7-10 days', 1),
('Ceftriaxone', '1-2g daily for 7-14 days', 1),

-- COVID-19
('Acetaminophen', '500-1000mg every 4-6 hours as needed', 2),
('Ibuprofen', '400-600mg every 4-6 hours as needed', 2),
('Vitamin C', '1000mg daily', 2),

-- Dengue
('Acetaminophen', '500-1000mg every 4-6 hours as needed', 3),
('Oral Rehydration Solution', 'As directed for hydration', 3),

-- Common Cold
('Dextromethorphan', '30mg every 4-6 hours as needed', 4),
('Pseudoephedrine', '60mg every 4-6 hours as needed', 4),
('Vitamin C', '1000mg daily', 4),

-- Asthma
('Albuterol Inhaler', '90mcg/puff as needed', 5),
('Salbutamol', '2-4mg three times daily', 5),

-- Gastroenteritis
('Loperamide', '2mg after each loose stool', 6),
('Oral Rehydration Solution', 'As directed', 6),

-- Migraine
('Sumatriptan', '50-100mg as needed', 7),
('Ibuprofen', '400-600mg every 4-6 hours', 7),

-- Conjunctivitis
('Chloramphenicol Eye Drops', '1-2 drops every 2-4 hours', 8),

-- Tonsillitis
('Penicillin V', '500mg four times daily for 10 days', 9),
('Amoxicillin', '500mg three times daily for 10 days', 9),

-- UTI
('Nitrofurantoin', '100mg twice daily for 5-7 days', 10),
('Ciprofloxacin', '250-500mg twice daily for 3 days', 10);

-- Insert sample precautions
INSERT INTO precautions (precaution_text, disease_id) VALUES
-- Pneumonia
('Consult doctor immediately', 1),
('Take prescribed medication as directed', 1),
('Rest and stay hydrated', 1),
('Follow up regularly with healthcare provider', 1),
('Avoid smoking and secondhand smoke', 1),

-- COVID-19
('Isolate yourself from others', 2),
('Monitor symptoms closely', 2),
('Stay hydrated and rest', 2),
('Contact healthcare provider if symptoms worsen', 2),
('Follow local health guidelines', 2),

-- Dengue
('Avoid NSAIDs (use only acetaminophen)', 3),
('Stay hydrated with oral rehydration solution', 3),
('Rest and avoid strenuous activity', 3),
('Monitor platelet count', 3),
('Seek immediate medical attention if severe symptoms', 3),

-- Common Cold
('Rest and stay hydrated', 4),
('Use over-the-counter medications as directed', 4),
('Avoid close contact with others', 4),
('Practice good hand hygiene', 4),

-- Asthma
('Avoid triggers (dust, smoke, pollen)', 5),
('Keep rescue inhaler with you', 5),
('Follow asthma action plan', 5),
('Regular check-ups with doctor', 5),
('Avoid strenuous exercise during attacks', 5),

-- Gastroenteritis
('Stay hydrated with clear fluids', 6),
('Eat bland foods (BRAT diet)', 6),
('Rest and avoid dairy products', 6),
('Practice good hand hygiene', 6),
('Seek medical attention if symptoms persist', 6),

-- Migraine
('Rest in a quiet, dark room', 7),
('Avoid trigger foods (chocolate, cheese, alcohol)', 7),
('Stay hydrated', 7),
('Practice stress management techniques', 7),

-- Conjunctivitis
('Avoid touching or rubbing eyes', 8),
('Wash hands frequently', 8),
('Avoid sharing towels or makeup', 8),
('Use prescribed eye drops as directed', 8),

-- Tonsillitis
('Rest voice and throat', 9),
('Stay hydrated with warm liquids', 9),
('Take prescribed antibiotics as directed', 9),
('Avoid spicy or acidic foods', 9),

-- UTI
('Drink plenty of water', 10),
('Urinate frequently', 10),
('Take prescribed antibiotics as directed', 10),
('Avoid caffeine and alcohol', 10),
('Practice good personal hygiene', 10);

