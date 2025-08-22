// Enhanced Patient Diagnosis System - Frontend
const API_BASE = 'http://localhost:8000/api'; // Enhanced API
const ENHANCED_API_BASE = 'http://localhost:8000/api'; // For new features

// Global state
let currentUser = null;
let availableSymptoms = [];
let selectedSymptoms = [];
let currentPatientId = null;

// API Helper Functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include', // For session cookies
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

async function enhancedApiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${ENHANCED_API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include',
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Enhanced API call failed:', error);
        throw error;
    }
}

// Utility Functions
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

function showLoading(show = true) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = show ? 'flex' : 'none';
    }
}

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Update navigation active state
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    
    // Find and activate the corresponding nav item
    const activeNavItem = document.querySelector(`[onclick="showSection('${sectionId}')"]`);
    if (activeNavItem) {
        activeNavItem.classList.add('active');
    }
}

// Enhanced Authentication Functions
async function loginUser(username, password) {
    try {
        showLoading(true);
        
        const response = await enhancedApiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        if (response.success) {
            currentUser = response.user;
            showMessage(`Welcome, ${currentUser.full_name}!`, 'success');
            
            // Update UI for logged-in user
            updateUIForLoggedInUser();
            
            // Show dashboard
            showSection('dashboard');
            loadDashboardData();
            
        } else {
            showMessage(response.error || 'Login failed', 'error');
        }
        
    } catch (error) {
        showMessage('Login failed: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function logout() {
    enhancedApiCall('/auth/logout', { method: 'POST' })
        .then(() => {
            currentUser = null;
            showMessage('Logged out successfully', 'success');
            updateUIForLoggedOutUser();
            showSection('welcome');
        })
        .catch(error => {
            console.error('Logout error:', error);
        });
}

function updateUIForLoggedInUser() {
    // Hide login nav, show dashboard navs
    document.getElementById('login-nav').style.display = 'none';
    document.getElementById('dashboard-nav').style.display = 'block';
    document.getElementById('patient-management-nav').style.display = 'block';
    document.getElementById('consultations-nav').style.display = 'block';
    
    // Update header
    const statusText = document.querySelector('.status-text');
    if (statusText) {
        statusText.textContent = `Logged in as ${currentUser.role}`;
    }
}

function updateUIForLoggedOutUser() {
    // Show login nav, hide dashboard navs
    document.getElementById('login-nav').style.display = 'block';
    document.getElementById('dashboard-nav').style.display = 'none';
    document.getElementById('patient-management-nav').style.display = 'none';
    document.getElementById('consultations-nav').style.display = 'none';
    
    // Update header
    const statusText = document.querySelector('.status-text');
    if (statusText) {
        statusText.textContent = 'System Online';
    }
}

// Dashboard Functions
async function loadDashboardData() {
    try {
        const [statsResponse, diseasesResponse, consultationsResponse] = await Promise.all([
            enhancedApiCall('/analytics/dashboard'),
            enhancedApiCall('/diseases'),
            enhancedApiCall('/consultations')
        ]);
        
        if (statsResponse.success) {
            displayDashboardStats(statsResponse.analytics);
        }
        
        if (diseasesResponse.success) {
            displayCommonDiseases(diseasesResponse.diseases);
        }
        
        if (consultationsResponse.success) {
            displayRecentConsultations(consultationsResponse.consultations);
        }
        
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        showMessage('Failed to load dashboard data', 'error');
    }
}

function displayDashboardStats(analytics) {
    const statsContent = document.getElementById('statsContent');
    if (!statsContent) return;
    
    statsContent.innerHTML = `
        <div class="stat-item">
            <span class="stat-number">${analytics.total_patients || 0}</span>
            <span class="stat-label">Total Patients</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">${analytics.today_consultations || 0}</span>
            <span class="stat-label">Today's Consultations</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">${analytics.month_consultations || 0}</span>
            <span class="stat-label">This Month</span>
        </div>
    `;
}

function displayCommonDiseases(diseases) {
    const diseasesContent = document.getElementById('diseasesContent');
    if (!diseasesContent) return;
    
    const topDiseases = diseases.slice(0, 5);
    diseasesContent.innerHTML = topDiseases.map(disease => `
        <div class="disease-item">
            <span class="disease-name">${disease.disease_name}</span>
            <span class="disease-description">${disease.description || 'No description available'}</span>
        </div>
    `).join('');
}

function displayRecentConsultations(consultations) {
    const consultationsContent = document.getElementById('consultationsContent');
    if (!consultationsContent) return;
    
    const recentConsultations = consultations.slice(0, 5);
    consultationsContent.innerHTML = recentConsultations.map(consultation => `
        <div class="consultation-item">
            <span class="consultation-date">${new Date(consultation.consultation_date).toLocaleDateString()}</span>
            <span class="consultation-patient">${consultation.patient_name || 'Unknown'}</span>
            <span class="consultation-status">${consultation.status}</span>
        </div>
    `).join('');
}

// Patient Management Functions
async function loadPatients() {
    try {
        showLoading(true);
        
        const response = await enhancedApiCall('/patients');
        
        if (response.success) {
            displayPatients(response.patients);
        } else {
            showMessage('Failed to load patients', 'error');
        }
        
    } catch (error) {
        console.error('Failed to load patients:', error);
        showMessage('Failed to load patients: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function displayPatients(patients) {
    const patientsList = document.getElementById('patientsList');
    if (!patientsList) return;
    
    if (patients.length === 0) {
        patientsList.innerHTML = '<div class="no-data">No patients found</div>';
        return;
    }
    
    patientsList.innerHTML = patients.map(patient => `
        <div class="patient-card" onclick="viewPatientDetails('${patient.registration_id}')">
            <div class="patient-header">
                <h4>${patient.name}</h4>
                <span class="patient-id">ID: ${patient.registration_id}</span>
            </div>
            <div class="patient-info">
                <p><strong>Age:</strong> ${patient.age} | <strong>Gender:</strong> ${patient.gender}</p>
                <p><strong>Contact:</strong> ${patient.contact}</p>
                <p><strong>Consultations:</strong> ${patient.consultation_count}</p>
                <p><strong>Last Visit:</strong> ${patient.last_visit ? new Date(patient.last_visit).toLocaleDateString() : 'Never'}</p>
            </div>
            <div class="patient-actions">
                <button onclick="viewPatientSummary('${patient.registration_id}')" class="action-btn">
                    View Summary
                </button>
                <button onclick="viewPatientConsultations('${patient.registration_id}')" class="action-btn">
                    Consultations
                </button>
            </div>
        </div>
    `).join('');
}

async function viewPatientSummary(patientId) {
    try {
        showLoading(true);
        
        const response = await enhancedApiCall(`/patients/${patientId}/summary`);
        
        if (response.success) {
            displayPatientSummary(response);
            showSection('consultations');
        } else {
            showMessage('Failed to load patient summary', 'error');
        }
        
    } catch (error) {
        console.error('Failed to load patient summary:', error);
        showMessage('Failed to load patient summary: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function displayPatientSummary(data) {
    const consultationsList = document.getElementById('consultationsList');
    if (!consultationsList) return;
    
    consultationsList.innerHTML = `
        <div class="patient-summary">
            <h3>Patient Summary: ${data.patient.name}</h3>
            <div class="summary-grid">
                <div class="summary-card">
                    <h4>Patient Information</h4>
                    <p><strong>ID:</strong> ${data.patient.registration_id}</p>
                    <p><strong>Age:</strong> ${data.patient.age}</p>
                    <p><strong>Gender:</strong> ${data.patient.gender}</p>
                    <p><strong>Contact:</strong> ${data.patient.contact}</p>
                </div>
                <div class="summary-card">
                    <h4>Consultation History</h4>
                    <p><strong>Total Consultations:</strong> ${data.total_consultations}</p>
                    <p><strong>Last Visit:</strong> ${data.consultations.length > 0 ? new Date(data.consultations[0].date).toLocaleDateString() : 'Never'}</p>
                </div>
            </div>
            
            <h4>Recent Consultations</h4>
            <div class="consultations-list">
                ${data.consultations.map(consultation => `
                    <div class="consultation-card">
                        <div class="consultation-header">
                            <span class="consultation-date">${new Date(consultation.date).toLocaleDateString()}</span>
                            <span class="consultation-confidence">${(consultation.confidence * 100).toFixed(1)}%</span>
                            <span class="consultation-status ${consultation.status}">${consultation.status}</span>
                        </div>
                        <div class="consultation-symptoms">
                            <strong>Symptoms:</strong> ${consultation.symptoms.join(', ')}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

async function viewPatientConsultations(patientId) {
    try {
        showLoading(true);
        
        const response = await enhancedApiCall(`/consultations/${patientId}`);
        
        if (response.success) {
            displayPatientConsultations(response.consultations, patientId);
            showSection('consultations');
        } else {
            showMessage('Failed to load consultations', 'error');
        }
        
    } catch (error) {
        console.error('Failed to load consultations:', error);
        showMessage('Failed to load consultations: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

function displayPatientConsultations(consultations, patientId) {
    const consultationsList = document.getElementById('consultationsList');
    if (!consultationsList) return;
    
    if (consultations.length === 0) {
        consultationsList.innerHTML = '<div class="no-data">No consultations found for this patient</div>';
        return;
    }
    
    consultationsList.innerHTML = `
        <div class="consultations-header">
            <h3>Consultation History</h3>
            <button onclick="createNewConsultation('${patientId}')" class="action-button">
                New Consultation
            </button>
        </div>
        
        <div class="consultations-grid">
            ${consultations.map(consultation => `
                <div class="consultation-card">
                    <div class="consultation-header">
                        <span class="consultation-date">${new Date(consultation.consultation_date).toLocaleDateString()}</span>
                        <span class="consultation-time">${new Date(consultation.consultation_date).toLocaleTimeString()}</span>
                        <span class="consultation-status ${consultation.status}">${consultation.status}</span>
                    </div>
                    
                    <div class="consultation-details">
                        <div class="consultation-section">
                            <h5>Symptoms Analyzed</h5>
                            <div class="symptoms-list">
                                ${consultation.symptoms_analyzed.map(symptom => 
                                    `<span class="symptom-tag">${symptom}</span>`
                                ).join('')}
                            </div>
                        </div>
                        
                        <div class="consultation-section">
                            <h5>Diagnosis Results</h5>
                            <div class="diagnosis-summary">
                                ${consultation.diagnosis_results && consultation.diagnosis_results.top_disease ? 
                                    `<strong>Primary Diagnosis:</strong> ${consultation.diagnosis_results.top_disease.name}<br>
                                     <strong>Confidence:</strong> ${(consultation.confidence_score * 100).toFixed(1)}%` :
                                    'No diagnosis available'
                                }
                            </div>
                        </div>
                        
                        ${consultation.doctor_notes ? `
                            <div class="consultation-section">
                                <h5>Doctor Notes</h5>
                                <p>${consultation.doctor_notes}</p>
                            </div>
                        ` : ''}
                        
                        ${consultation.follow_up_date ? `
                            <div class="consultation-section">
                                <h5>Follow-up Date</h5>
                                <p>${new Date(consultation.follow_up_date).toLocaleDateString()}</p>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

// Existing Functions (Enhanced)
async function setupPatientForm() {
    const form = document.getElementById('patientForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const patientData = {
            name: formData.get('name'),
            age: parseInt(formData.get('age')),
            gender: formData.get('gender'),
            contact: formData.get('contact')
        };
        
        try {
            showLoading(true);
            
            // Example fetch to Flask API
            fetch('http://localhost:8000/api/patient/register', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ name, age, gender, contact })
            })
            .then(res => res.json())
            .then(data => console.log(data));
            
            const response = await apiCall('/patient/register', {
                method: 'POST',
                body: JSON.stringify(patientData)
            });
            
            if (response.success) {
                currentPatientId = response.registration_id;
                localStorage.setItem('currentPatientId', currentPatientId);
                
                showMessage(`Patient registered successfully! ID: ${response.registration_id}`, 'success');
                
                // Show registration result
                const resultDiv = document.getElementById('registrationResult');
                if (resultDiv) {
                    resultDiv.innerHTML = `
                        <div class="success-message">
                            <h3>✅ Registration Successful!</h3>
                            <p><strong>Patient ID:</strong> ${response.registration_id}</p>
                            <p><strong>Name:</strong> ${patientData.name}</p>
                            <p>You can now proceed to symptom analysis.</p>
                            <button onclick="showSection('symptom-analysis')" class="action-button">
                                Continue to Symptoms
                            </button>
                        </div>
                    `;
                    resultDiv.style.display = 'block';
                }
                
                // Reset form
                form.reset();
                
            } else {
                showMessage(response.error || 'Registration failed', 'error');
            }
            
        } catch (error) {
            console.error('Registration error:', error);
            showMessage('Registration failed: ' + error.message, 'error');
        } finally {
            showLoading(false);
        }
    });
}

async function setupSymptomInput() {
    const searchInput = document.getElementById('symptomSearch');
    const suggestionsDiv = document.getElementById('symptomSuggestions');
    
    if (!searchInput || !suggestionsDiv) return;
    
    // Load available symptoms
    await loadAvailableSymptoms();
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        if (query.length > 0) {
            displaySymptomSuggestions(query);
        } else {
            suggestionsDiv.style.display = 'none';
        }
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
            suggestionsDiv.style.display = 'none';
        }
    });
}

async function loadAvailableSymptoms() {
    try {
        const response = await apiCall('/symptoms');
        if (response.success) {
            availableSymptoms = response.symptoms;
        }
    } catch (error) {
        console.error('Failed to load symptoms:', error);
    }
}

function displaySymptomSuggestions(query) {
    const suggestionsDiv = document.getElementById('symptomSuggestions');
    if (!suggestionsDiv) return;
    
    const filteredSymptoms = availableSymptoms.filter(symptom => 
        symptom.toLowerCase().includes(query.toLowerCase())
    );
    
    if (filteredSymptoms.length > 0) {
        suggestionsDiv.innerHTML = filteredSymptoms.map(symptom => 
            `<div class="suggestion-item" onclick="addSymptom('${symptom}')">${symptom}</div>`
        ).join('');
        suggestionsDiv.style.display = 'block';
    } else {
        suggestionsDiv.style.display = 'none';
    }
}

function addSymptom(symptom) {
    if (!selectedSymptoms.includes(symptom)) {
        selectedSymptoms.push(symptom);
        updateSelectedSymptomsDisplay();
        updateAnalyzeButton();
    }
    
    // Clear search and hide suggestions
    const searchInput = document.getElementById('symptomSearch');
    const suggestionsDiv = document.getElementById('symptomSuggestions');
    if (searchInput) searchInput.value = '';
    if (suggestionsDiv) suggestionsDiv.style.display = 'none';
}

function removeSymptom(symptom) {
    selectedSymptoms = selectedSymptoms.filter(s => s !== symptom);
    updateSelectedSymptomsDisplay();
    updateAnalyzeButton();
}

function updateSelectedSymptomsDisplay() {
    const symptomsList = document.getElementById('selectedSymptomsList');
    if (!symptomsList) return;
    
    symptomsList.innerHTML = selectedSymptoms.map(symptom => `
        <span class="symptom-tag">
            ${symptom}
            <button onclick="removeSymptom('${symptom}')" class="remove-symptom">×</button>
        </span>
    `).join('');
}

function updateAnalyzeButton() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = selectedSymptoms.length === 0;
    }
}

async function analyzeSymptoms() {
    if (selectedSymptoms.length === 0) {
        showMessage('Please select at least one symptom', 'error');
        return;
    }
    
    if (!currentPatientId) {
        showMessage('Please register as a patient first', 'error');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await apiCall('/diagnose', {
            method: 'POST',
            body: JSON.stringify({
                symptoms: selectedSymptoms,
                patient_id: currentPatientId
            })
        });
        
        if (response.success) {
            displayDiagnosisResults(response.results);
            
            // Create consultation record
            if (currentUser && ['doctor', 'nurse', 'admin'].includes(currentUser.role)) {
                await createConsultationRecord(response.results);
            }
            
        } else {
            showMessage(response.error || 'Diagnosis failed', 'error');
        }
        
    } catch (error) {
        console.error('Diagnosis error:', error);
        showMessage('Diagnosis failed: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function createConsultationRecord(diagnosisResults) {
    try {
        const consultationData = {
            patient_id: currentPatientId,
            symptoms: selectedSymptoms,
            diagnosis_results: diagnosisResults,
            confidence_score: diagnosisResults.top_disease ? diagnosisResults.top_disease.confidence : 0.0,
            doctor_notes: `Diagnosis performed by ${currentUser.full_name} (${currentUser.role})`,
            follow_up_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] // 1 week from now
        };
        
        await enhancedApiCall('/consultations', {
            method: 'POST',
            body: JSON.stringify(consultationData)
        });
        
        showMessage('Consultation record created successfully', 'success');
        
    } catch (error) {
        console.error('Failed to create consultation record:', error);
    }
}

function displayDiagnosisResults(results) {
    const resultDiv = document.getElementById('diagnosisResult');
    if (!resultDiv) return;
    
    const topDisease = results.top_disease;
    
    resultDiv.innerHTML = `
        <div class="diagnosis-summary">
            <h3>🔍 Diagnosis Results</h3>
            ${topDisease ? `
                <div class="primary-diagnosis">
                    <h4>Primary Diagnosis: ${topDisease.name}</h4>
                    <p><strong>Confidence:</strong> ${(topDisease.confidence * 100).toFixed(1)}%</p>
                    <p><strong>Description:</strong> ${topDisease.description || 'No description available'}</p>
                </div>
                
                <div class="diagnosis-details">
                    <h4>Matched Symptoms:</h4>
                    <div class="matched-symptoms">
                        ${topDisease.matched_symptoms.map(symptom => 
                            `<span class="symptom-tag matched">${symptom}</span>`
                        ).join('')}
                    </div>
                    
                    <h4>Medications:</h4>
                    <div class="medications-list">
                        ${topDisease.medicines.map(medicine => 
                            `<div class="medicine-item">
                                <strong>${medicine.name}</strong> - ${medicine.dosage}
                            </div>`
                        ).join('')}
                    </div>
                    
                    <h4>Precautions:</h4>
                    <div class="precautions-list">
                        ${topDisease.precautions.map(precaution => 
                            `<div class="precaution-item">• ${precaution}</div>`
                        ).join('')}
                    </div>
                </div>
            ` : `
                <div class="no-diagnosis">
                    <p>No specific diagnosis found for the given symptoms.</p>
                    <p>Please consult a healthcare professional for proper evaluation.</p>
                </div>
            `}
        </div>
    `;
    
    resultDiv.style.display = 'block';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Enhanced Patient Diagnosis System Loaded!');
    
    // Setup existing features
    setupPatientForm();
    setupSymptomInput();
    
    // Setup new features
    setupLoginForm();
    setupPatientSearch();
    
    // Check if user is already logged in
    checkAuthStatus();
    
    // Show welcome section by default
    showSection('welcome');
});

function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(loginForm);
        const username = formData.get('username');
        const password = formData.get('password');
        
        await loginUser(username, password);
    });
}

function setupPatientSearch() {
    const searchInput = document.getElementById('patientSearchInput');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        if (query.length > 0) {
            // Implement search functionality
            filterPatients(query);
        } else {
            loadPatients();
        }
    });
}

async function filterPatients(query) {
    try {
        const response = await enhancedApiCall('/patients');
        
        if (response.success) {
            const filteredPatients = response.patients.filter(patient => 
                patient.name.toLowerCase().includes(query.toLowerCase()) ||
                patient.registration_id.toLowerCase().includes(query.toLowerCase())
            );
            
            displayPatients(filteredPatients);
        }
        
    } catch (error) {
        console.error('Search failed:', error);
    }
}

async function checkAuthStatus() {
    try {
        const response = await enhancedApiCall('/auth/profile');
        
        if (response.success) {
            currentUser = response.user;
            updateUIForLoggedInUser();
        }
        
    } catch (error) {
        // User not logged in, keep default UI
        console.log('User not authenticated');
    }
}

// Mobile sidebar toggle
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContainer = document.querySelector('.main-container');
    
    if (sidebar && mainContainer) {
        sidebar.classList.toggle('sidebar-open');
        mainContainer.classList.toggle('sidebar-open');
    }
}

// Export functions for global access
window.showSection = showSection;
window.analyzeSymptoms = analyzeSymptoms;
window.logout = logout;
window.viewPatientDetails = viewPatientSummary;
window.viewPatientSummary = viewPatientSummary;
window.viewPatientConsultations = viewPatientConsultations;
window.createNewConsultation = (patientId) => {
    showMessage('New consultation feature coming soon!', 'info');
};
window.toggleSidebar = toggleSidebar;