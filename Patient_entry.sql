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
    disease_name VARCHAR(50)
);

CREATE TABLE disease_symptom (
    disease_id INT,
    symptom_name VARCHAR(50),
    FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
);

