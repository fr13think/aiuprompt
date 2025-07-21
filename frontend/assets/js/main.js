/**
 * Pastikan seluruh dokumen HTML sudah dimuat sebelum menjalankan JavaScript
 */
document.addEventListener('DOMContentLoaded', () => {

    // === DEKLARASI ELEMEN ===
    // Form utama
    const promptForm = document.getElementById('prompt-form');
    const promptInput = document.getElementById('prompt-input');
    const analyzeButton = document.getElementById('analyze-button');
    const buttonText = document.querySelector('.button-text');
    const spinner = document.querySelector('.spinner');
    const targetModelSelect = document.getElementById('target-model');

    // Elemen Template
    const openTemplatesBtn = document.getElementById('open-templates-btn');
    const closeTemplatesBtn = document.getElementById('close-templates-btn');
    const templatesModal = document.getElementById('templates-modal');
    const templatesList = document.getElementById('templates-list');

    // Elemen Otentikasi
    const authContainer = document.getElementById('auth-container');
    const authBtn = document.getElementById('auth-btn');
    const userInfo = document.getElementById('user-info');
    const logoutBtn = document.getElementById('logout-btn');
    const authModal = document.getElementById('auth-modal');
    const closeAuthBtn = document.getElementById('close-auth-btn');
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const authError = document.getElementById('auth-error');

    // Elemen Kontainer Hasil & Error
    const resultsContainer = document.getElementById('results-container');
    const errorContainer = document.getElementById('error-container');
    const errorMessageElem = document.getElementById('error-message');

    // Elemen Spesifik Hasil
    // ... (Elemen hasil tetap sama)
    const copyButton = document.getElementById('copy-button');

    let userToken = null;


    // === FUNGSI UTAMA & INSIALISASI ===

    function checkLoginStatus() {
        userToken = localStorage.getItem('userToken');
        const userEmail = localStorage.getItem('userEmail');

        if (userToken && userEmail) {
            authBtn.classList.add('hidden');
            userInfo.textContent = `Welcome, ${userEmail}`;
            userInfo.classList.remove('hidden');
            logoutBtn.classList.remove('hidden');
        } else {
            authBtn.classList.remove('hidden');
            userInfo.classList.add('hidden');
            logoutBtn.classList.add('hidden');
        }
    }

    // Panggil saat halaman dimuat
    checkLoginStatus();


    // === EVENT LISTENERS ===

    // Event Listener utama untuk form analisis prompt
    promptForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        // ... (Logika form submit sama seperti sebelumnya) ...
        const promptText = promptInput.value.trim();
        const selectedModel = targetModelSelect.value;
        if (promptText.length < 20) {
            showError("Input prompt terlalu pendek. Harap masukkan minimal 20 karakter.");
            return;
        }
        setLoadingState(true);
        hideResults();
        hideError();
        try {
            const analysisData = await api.analyzePrompt(promptText, selectedModel);
            displayResults(analysisData);
        } catch (error) {
            showError(error.message);
        } finally {
            setLoadingState(false);
        }
    });

    // Event Listeners untuk Otentikasi
    authBtn.addEventListener('click', () => authModal.classList.remove('hidden'));
    closeAuthBtn.addEventListener('click', () => authModal.classList.add('hidden'));
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('userToken');
        localStorage.removeItem('userEmail');
        userToken = null;
        checkLoginStatus();
    });

    loginTab.addEventListener('click', () => {
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        hideAuthError();
    });

    registerTab.addEventListener('click', () => {
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        hideAuthError();
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAuthError();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        try {
            const data = await api.loginUser(email, password);
            localStorage.setItem('userToken', data.access_token);
            localStorage.setItem('userEmail', email);
            authModal.classList.add('hidden');
            checkLoginStatus();
        } catch (error) {
            showAuthError(error.message);
        }
    });

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAuthError();
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        try {
            await api.registerUser(email, password);
            // Otomatis login setelah register berhasil
            const data = await api.loginUser(email, password);
            localStorage.setItem('userToken', data.access_token);
            localStorage.setItem('userEmail', email);
            authModal.classList.add('hidden');
            checkLoginStatus();
        } catch (error) {
            showAuthError(error.message);
        }
    });

    /**
     * Event listener untuk tombol 'Salin'
     */
    copyButton.addEventListener('click', () => {
        const textToCopy = optimizedPromptElem.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
            copyButton.textContent = 'Disalin!';
            setTimeout(() => {
                copyButton.textContent = 'Salin';
            }, 2000);
        }).catch(err => {
            console.error('Gagal menyalin teks: ', err);
            alert("Gagal menyalin. Silakan salin secara manual.");
        });
    });

    /**
     * Event listener untuk membuka modal template
     */
    openTemplatesBtn.addEventListener('click', async () => {
        try {
            const templates = await api.getTemplates();
            templatesList.innerHTML = ''; // Kosongkan daftar
            templates.forEach(template => {
                const item = document.createElement('div');
                item.className = 'template-item';
                item.innerHTML = `<h4>${template.title}</h4><p>${template.prompt}</p>`;
                item.addEventListener('click', () => {
                    promptInput.value = template.prompt;
                    templatesModal.classList.add('hidden');
                });
                templatesList.appendChild(item);
            });
            templatesModal.classList.remove('hidden');
        } catch (error) {
            showError(error.message);
        }
    });

    /**
     * Event listener untuk menutup modal template
     */
    closeTemplatesBtn.addEventListener('click', () => templatesModal.classList.add('hidden'));
    templatesModal.addEventListener('click', (e) => {
        if (e.target === templatesModal) {
            templatesModal.classList.add('hidden');
        }
    });


    // === FUNGSI BANTU ===

    function showAuthError(message) {
        authError.textContent = message;
        authError.classList.remove('hidden');
    }

    function hideAuthError() {
        authError.classList.add('hidden');
    }

    function setLoadingState(isLoading) {
        analyzeButton.disabled = isLoading;
        buttonText.style.display = isLoading ? 'none' : 'block';
        spinner.style.display = isLoading ? 'block' : 'none';
    }

    function displayResults(data) {
        clarityScoreElem.textContent = `${data.clarity_score}/10`;
        specificityScoreElem.textContent = `${data.specificity_score}/10`;
        techniqueAnalysisElem.innerHTML = `<strong>Teknik Terdeteksi:</strong> ${data.technique_analysis.detected_techniques.join(', ')}<br><em>${data.technique_analysis.explanation}</em>`;
        ambiguityPotentialElem.textContent = data.ambiguity_potential;
        improvementSuggestionsElem.innerHTML = '';
        data.improvement_suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            improvementSuggestionsElem.appendChild(li);
        });
        optimizedPromptElem.textContent = data.optimized_prompt;
        resultsContainer.classList.remove('hidden');
    }

    function hideResults() {
        resultsContainer.classList.add('hidden');
    }

    function showError(message) {
        errorMessageElem.textContent = message;
        errorContainer.classList.remove('hidden');
    }

    function hideError() {
        errorContainer.classList.add('hidden');
    }
});