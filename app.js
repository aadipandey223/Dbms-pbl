// Toggle sidebar function
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("active");
}

// API base URL
const API_BASE = 'http://localhost:5000/api';

// API helper functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get all buttons
    const symptomBtn = document.getElementById('symptomBtn');
    const medicationBtn = document.getElementById('medicationBtn');
    const precautionBtn = document.getElementById('precautionBtn');
    const historyBtn = document.getElementById('historyBtn');
    const aboutBtn = document.getElementById('aboutBtn');
    const mainContent = document.getElementById('mainContent');
    
    // Symptom Analysis button click event
    symptomBtn.addEventListener('click', function() {
        mainContent.innerHTML = `
            <div class="section-content">
                <h2><i class="fas fa-notes-medical"></i> Symptom Analysis</h2>
                <p>Enter your symptoms below to get a possible diagnosis.</p>
                
                <!-- Patient Registration Form -->
                <div class="patient-form">
                    <h3><i class="fas fa-user-plus"></i> Patient Registration</h3>
                    <form id="patientForm">
                        <div class="form-row">
                            <input type="text" id="patientName" placeholder="Full Name" required>
                            <select id="patientGender" required>
                                <option value="">Select Gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Other</option>
                            </select>
                        </div>
                        <div class="form-row">
                            <input type="number" id="patientAge" placeholder="Age" min="1" max="120" required>
                            <input type="tel" id="patientContact" placeholder="Contact Number" required>
                        </div>
                        <button type="submit" class="action-btn"><i class="fas fa-user-plus"></i> Register Patient</button>
                    </form>
                </div>

                <!-- Symptom Input Section -->
                <div class="symptom-input-section" style="display: none;">
                    <h3><i class="fas fa-notes-medical"></i> Enter Your Symptoms</h3>
                    <div class="symptom-search">
                        <input type="text" id="symptomSearch" placeholder="Type symptom (e.g., fever, cough)">
                        <div id="symptomSuggestions" class="symptom-suggestions"></div>
                    </div>
                    <div class="selected-symptoms">
                        <h4>Selected Symptoms:</h4>
                        <div id="selectedSymptomsList"></div>
                    </div>
                    <button id="analyzeBtn" class="action-btn" disabled><i class="fas fa-search"></i> Analyze Symptoms</button>
                </div>

                <div id="diagnosisResult" class="result-container"></div>
            </div>
        `;
        
        // Add event listeners
        setupPatientForm();
        setupSymptomInput();
        
        // Close sidebar on mobile after selection
        if (window.innerWidth <= 768) {
            toggleSidebar();
        }
    });
    
    // Medications button click event
    medicationBtn.addEventListener('click', function() {
        mainContent.innerHTML = `
            <div class="section-content">
                <h2><i class="fas fa-pills"></i> Medication Guide</h2>
                <p>Search for medications by disease or browse common medications below.</p>
                <div class="input-container">
                    <input type="text" id="medicationSearch" placeholder="Search by disease (e.g., Pneumonia, COVID-19)">
                    <button class="action-btn" onclick="searchMedications()"><i class="fas fa-search"></i> Search</button>
                </div>
                <div id="medicationsList" class="medications-list">
                    <div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading medications...</div>
                </div>
            </div>
        `;
        
        // Load all diseases and medications
        loadDiseasesAndMedications();
        
        // Close sidebar on mobile after selection
        if (window.innerWidth <= 768) {
            toggleSidebar();
        }
    });
    
    // Precautions button click event
    precautionBtn.addEventListener('click', function() {
        mainContent.innerHTML = `
            <div class="section-content">
                <h2><i class="fas fa-shield-alt"></i> Precautions</h2>
                <p>Learn about preventive measures for various diseases.</p>
                <div id="precautionsList" class="precautions-list">
                    <div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading precautions...</div>
                </div>
            </div>
        `;
        
        // Load all diseases and precautions
        loadDiseasesAndPrecautions();
        
        // Close sidebar on mobile after selection
        if (window.innerWidth <= 768) {
            toggleSidebar();
        }
    });
    
    // Patient History button click event
    historyBtn.addEventListener('click', function() {
        mainContent.innerHTML = `
            <div class="section-content">
                <h2><i class="fas fa-history"></i> Patient History</h2>
                <p>View your previous diagnoses and consultations.</p>
                <div class="history-list">
                    <div class="history-card">
                        <div class="history-date">Coming Soon</div>
                        <h3>Patient History Feature</h3>
                        <p>This feature will be available in the next update to track patient consultation history.</p>
                    </div>
                </div>
            </div>
        `;
        
        // Close sidebar on mobile after selection
        if (window.innerWidth <= 768) {
            toggleSidebar();
        }
    });
    
    // About System button click event
    aboutBtn.addEventListener('click', function() {
        mainContent.innerHTML = `
            <div class="section-content about-section">
                <h2><i class="fas fa-info-circle"></i> About MediCare Hospital System</h2>
                <p>MediCare Hospital System is an intelligent healthcare platform designed to help diagnose diseases based on symptoms and provide medication recommendations.</p>
                <div class="about-details">
                    <div class="about-card">
                        <i class="fas fa-brain"></i>
                        <h3>AI-Powered Diagnosis</h3>
                        <p>Our system uses advanced algorithms to analyze symptoms and provide accurate disease predictions based on medical databases.</p>
                    </div>
                    <div class="about-card">
                        <i class="fas fa-database"></i>
                        <h3>Comprehensive Database</h3>
                        <p>Access information on various diseases, medications, and precautions from our extensive medical database.</p>
                    </div>
                    <div class="about-card">
                        <i class="fas fa-user-md"></i>
                        <h3>Medical Expertise</h3>
                        <p>Developed in collaboration with healthcare professionals to ensure accuracy and reliability.</p>
                    </div>
                </div>
                <div class="disclaimer-box">
                    <h3><i class="fas fa-exclamation-triangle"></i> Important Disclaimer</h3>
                    <p>This system is designed to assist with preliminary diagnosis and should not replace professional medical advice. Always consult with a qualified healthcare provider for proper diagnosis and treatment.</p>
                </div>
            </div>
        `;
        
        // Close sidebar on mobile after selection
        if (window.innerWidth <= 768) {
            toggleSidebar();
        }
    });
});

// Setup patient registration form
function setupPatientForm() {
    const form = document.getElementById('patientForm');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('patientName').value,
            gender: document.getElementById('patientGender').value,
            age: parseInt(document.getElementById('patientAge').value),
            contact: document.getElementById('patientContact').value
        };
        
        try {
            const response = await apiCall('/patient/register', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            
            if (response.success) {
                // Store registration ID
                localStorage.setItem('currentPatientId', response.registration_id);
                
                // Show success message and enable symptom input
                showMessage(`✅ Patient registered successfully! ID: ${response.registration_id}`, 'success');
                
                // Hide form and show symptom input
                document.querySelector('.patient-form').style.display = 'none';
                document.querySelector('.symptom-input-section').style.display = 'block';
                
                // Load available symptoms
                loadAvailableSymptoms();
            } else {
                showMessage(`❌ Registration failed: ${response.error}`, 'error');
            }
        } catch (error) {
            showMessage(`❌ Registration failed: ${error.message}`, 'error');
        }
    });
}

// Setup symptom input functionality
function setupSymptomInput() {
    const symptomSearch = document.getElementById('symptomSearch');
    const analyzeBtn = document.getElementById('analyzeBtn');
    let selectedSymptoms = [];
    
    // Symptom search with suggestions
    symptomSearch.addEventListener('input', async function() {
        const query = this.value.trim();
        if (query.length < 2) {
            document.getElementById('symptomSuggestions').innerHTML = '';
            return;
        }
        
        try {
            const response = await apiCall(`/symptoms/suggest?q=${encodeURIComponent(query)}`);
            if (response.success) {
                displaySymptomSuggestions(response.suggestions);
            }
        } catch (error) {
            console.error('Failed to get symptom suggestions:', error);
        }
    });
    
    // Analyze symptoms button
    analyzeBtn.addEventListener('click', async function() {
        if (selectedSymptoms.length === 0) {
            showMessage('❌ Please select at least one symptom', 'error');
            return;
        }
        
        try {
            const response = await apiCall('/diagnose', {
                method: 'POST',
                body: JSON.stringify({ symptoms: selectedSymptoms })
            });
            
            if (response.success) {
                displayDiagnosisResults(response.diagnosis, selectedSymptoms);
            } else {
                showMessage(`❌ Diagnosis failed: ${response.error}`, 'error');
            }
        } catch (error) {
            showMessage(`❌ Diagnosis failed: ${error.message}`, 'error');
        }
    });
}

// Display symptom suggestions
function displaySymptomSuggestions(suggestions) {
    const suggestionsDiv = document.getElementById('symptomSuggestions');
    suggestionsDiv.innerHTML = '';
    
    suggestions.forEach(symptom => {
        const div = document.createElement('div');
        div.className = 'symptom-suggestion';
        div.textContent = symptom;
        div.onclick = () => addSymptom(symptom);
        suggestionsDiv.appendChild(div);
    });
}

// Add symptom to selected list
function addSymptom(symptom) {
    const selectedSymptomsList = document.getElementById('selectedSymptomsList');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    if (!selectedSymptoms.includes(symptom)) {
        selectedSymptoms.push(symptom);
        
        const symptomTag = document.createElement('span');
        symptomTag.className = 'symptom-tag';
        symptomTag.innerHTML = `${symptom} <i class="fas fa-times" onclick="removeSymptom('${symptom}', this)"></i>`;
        selectedSymptomsList.appendChild(symptomTag);
        
        // Enable analyze button
        analyzeBtn.disabled = false;
        
        // Clear search
        document.getElementById('symptomSearch').value = '';
        document.getElementById('symptomSuggestions').innerHTML = '';
    }
}

// Remove symptom from selected list
function removeSymptom(symptom, element) {
    selectedSymptoms = selectedSymptoms.filter(s => s !== symptom);
    element.parentElement.remove();
    
    // Disable analyze button if no symptoms
    if (selectedSymptoms.length === 0) {
        document.getElementById('analyzeBtn').disabled = true;
    }
}

// Load available symptoms
async function loadAvailableSymptoms() {
    try {
        const response = await apiCall('/symptoms');
        if (response.success) {
            console.log(`Loaded ${response.count} available symptoms`);
        }
    } catch (error) {
        console.error('Failed to load symptoms:', error);
    }
}

// Display diagnosis results
function displayDiagnosisResults(diagnosis, symptoms) {
    const resultDiv = document.getElementById('diagnosisResult');
    
    let html = `
        <div class="diagnosis-summary">
            <h3><i class="fas fa-clipboard-list"></i> Analysis Summary</h3>
            <p><strong>Symptoms analyzed:</strong> ${symptoms.join(', ')}</p>
            <p><strong>Diseases found:</strong> ${diagnosis.length}</p>
        </div>
    `;
    
    diagnosis.forEach((result, index) => {
        const disease = result.disease;
        html += `
            <div class="diagnosis-card">
                <h3><i class="fas fa-heartbeat"></i> ${index + 1}. ${disease.name} (Score: ${result.weighted_score}%)</h3>
                <p class="diagnosis-description">${disease.description}</p>
                <div class="diagnosis-details">
                    <div class="detail-section">
                        <h4><i class="fas fa-check-circle"></i> Matched Symptoms:</h4>
                        <p>${result.matched_symptoms.join(', ')}</p>
                        <p><strong>Match percentage:</strong> ${result.match_percentage}%</p>
                    </div>
                    
                    ${result.medicines.length > 0 ? `
                        <div class="detail-section">
                            <h4><i class="fas fa-pills"></i> Recommended Medications:</h4>
                            <ul>
                                ${result.medicines.map(med => `<li><strong>${med.name}</strong> - ${med.dosage}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${result.precautions.length > 0 ? `
                        <div class="detail-section">
                            <h4><i class="fas fa-shield-alt"></i> Recommended Precautions:</h4>
                            <ul>
                                ${result.precautions.map(precaution => `<li>${precaution}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    });
    
    html += `
        <div class="disclaimer">
            <p><i class="fas fa-exclamation-triangle"></i> <strong>Note:</strong> This is a preliminary diagnosis based on symptom analysis. Please consult with a healthcare professional for proper medical advice and treatment.</p>
        </div>
    `;
    
    resultDiv.innerHTML = html;
}

// Load diseases and medications
async function loadDiseasesAndMedications() {
    try {
        const response = await apiCall('/diseases');
        if (response.success) {
            displayMedications(response.diseases);
        }
    } catch (error) {
        document.getElementById('medicationsList').innerHTML = `<div class="error">❌ Failed to load medications: ${error.message}</div>`;
    }
}

// Display medications
function displayMedications(diseases) {
    const container = document.getElementById('medicationsList');
    
    let html = '';
    diseases.forEach(disease => {
        html += `
            <div class="medication-card">
                <h3>${disease.name}</h3>
                <p class="disease-description">${disease.description}</p>
                <div class="medication-info">
                    <p><i class="fas fa-info-circle"></i> Click to view medications</p>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Load diseases and precautions
async function loadDiseasesAndPrecautions() {
    try {
        const response = await apiCall('/diseases');
        if (response.success) {
            displayPrecautions(response.diseases);
        }
    } catch (error) {
        document.getElementById('precautionsList').innerHTML = `<div class="error">❌ Failed to load precautions: ${error.message}</div>`;
    }
}

// Display precautions
function displayPrecautions(diseases) {
    const container = document.getElementById('precautionsList');
    
    let html = '';
    diseases.forEach(disease => {
        html += `
            <div class="precaution-card">
                <h3>${disease.name}</h3>
                <p class="disease-description">${disease.description}</p>
                <div class="precaution-info">
                    <p><i class="fas fa-info-circle"></i> Click to view precautions</p>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Show message to user
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    document.body.appendChild(messageDiv);
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}