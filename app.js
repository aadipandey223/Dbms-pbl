// Toggle sidebar function
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("active");
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
                <div class="input-container">
                    <textarea id="symptomsInput" placeholder="Enter symptoms separated by commas (e.g., fever, cough, headache)"></textarea>
                    <button id="analyzeBtn" class="action-btn"><i class="fas fa-search"></i> Analyze Symptoms</button>
                </div>
                <div id="diagnosisResult" class="result-container"></div>
            </div>
        `;
        
        // Add event listener to the analyze button
        document.getElementById('analyzeBtn').addEventListener('click', function() {
            const symptoms = document.getElementById('symptomsInput').value;
            if (symptoms.trim() === '') {
                alert('Please enter symptoms');
                return;
            }
            
            // Simulate diagnosis (in a real app, this would call the Python backend)
            const diagnosisResult = document.getElementById('diagnosisResult');
            diagnosisResult.innerHTML = `<div class="loading"><i class="fas fa-spinner fa-spin"></i> Analyzing symptoms...</div>`;
            
            setTimeout(() => {
                diagnosisResult.innerHTML = `
                    <div class="diagnosis-card">
                        <h3><i class="fas fa-heartbeat"></i> Possible Diagnosis</h3>
                        <p class="diagnosis-name">Pneumonia</p>
                        <div class="diagnosis-details">
                            <div class="detail-section">
                                <h4><i class="fas fa-shield-alt"></i> Recommended Precautions:</h4>
                                <ul>
                                    <li>Consult doctor immediately</li>
                                    <li>Take prescribed medication</li>
                                    <li>Rest and stay hydrated</li>
                                    <li>Follow up regularly</li>
                                </ul>
                            </div>
                            <div class="detail-section">
                                <h4><i class="fas fa-pills"></i> Recommended Medications:</h4>
                                <ul>
                                    <li><strong>Azithromycin</strong> - 500mg once daily for 3-5 days</li>
                                </ul>
                            </div>
                        </div>
                        <p class="disclaimer">Note: This is a simulated result. Please consult with a healthcare professional for proper medical advice.</p>
                    </div>
                `;
            }, 2000);
        });
        
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
                    <button class="action-btn"><i class="fas fa-search"></i> Search</button>
                </div>
                <div class="medications-list">
                    <div class="medication-card">
                        <h3>Pneumonia</h3>
                        <p><strong>Azithromycin</strong> - 500mg</p>
                        <p>Take once daily for 3-5 days</p>
                    </div>
                    <div class="medication-card">
                        <h3>COVID-19</h3>
                        <p><strong>Acetaminophen</strong> - 500mg</p>
                        <p>Take as needed for fever or pain</p>
                    </div>
                    <div class="medication-card">
                        <h3>Dengue</h3>
                        <p><strong>Acetaminophen</strong> - 500mg</p>
                        <p>Take as needed for fever or pain (avoid NSAIDs)</p>
                    </div>
                </div>
            </div>
        `;
        
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
                <div class="precautions-list">
                    <div class="precaution-card">
                        <h3>Pneumonia</h3>
                        <ul>
                            <li>Consult doctor</li>
                            <li>Take medication as prescribed</li>
                            <li>Rest and stay hydrated</li>
                            <li>Follow up regularly</li>
                        </ul>
                    </div>
                    <div class="precaution-card">
                        <h3>Heart Attack</h3>
                        <ul>
                            <li>Maintain healthy diet</li>
                            <li>Regular exercise</li>
                            <li>Avoid smoking</li>
                            <li>Regular check-ups</li>
                        </ul>
                    </div>
                    <div class="precaution-card">
                        <h3>Anemia</h3>
                        <ul>
                            <li>Iron-rich diet</li>
                            <li>Vitamin supplements</li>
                            <li>Regular blood tests</li>
                            <li>Consult doctor</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        
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
                        <div class="history-date">July 28, 2025</div>
                        <h3>Diagnosis: Bronchial Asthma</h3>
                        <p><strong>Symptoms:</strong> cough, fever, fatigue, shortness of breath</p>
                        <p><strong>Medications:</strong> Albuterol Inhaler - 90mcg/puff</p>
                    </div>
                    <div class="history-card">
                        <div class="history-date">June 15, 2025</div>
                        <h3>Diagnosis: Dengue</h3>
                        <p><strong>Symptoms:</strong> fever, headache, muscle pain, joint pain, skin rash</p>
                        <p><strong>Medications:</strong> Acetaminophen - 500mg</p>
                    </div>
                    <div class="history-card">
                        <div class="history-date">May 3, 2025</div>
                        <h3>Diagnosis: Common Cold</h3>
                        <p><strong>Symptoms:</strong> sneezing, runny nose, cough, sore throat</p>
                        <p><strong>Medications:</strong> Dextromethorphan - 30mg</p>
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
                        <p>Our system uses machine learning algorithms to analyze symptoms and provide accurate disease predictions.</p>
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