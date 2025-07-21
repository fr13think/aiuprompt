/**
 * Pastikan seluruh dokumen HTML sudah dimuat sebelum menjalankan JavaScript
 */
document.addEventListener('DOMContentLoaded', () => {

    // === DEKLARASI ELEMEN ===
    const promptForm = document.getElementById('prompt-form');
    if (!promptForm) {
        console.error("Kesalahan Kritis: Elemen form dengan ID 'prompt-form' tidak ditemukan.");
        return; // Hentikan eksekusi jika elemen utama tidak ada
    }
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

    // Elemen Kontainer Hasil & Error
    const resultsContainer = document.getElementById('results-container');
    const errorContainer = document.getElementById('error-container');
    const errorMessageElem = document.getElementById('error-message');

    // Elemen Spesifik Hasil
    const clarityScoreElem = document.getElementById('clarity-score');
    const specificityScoreElem = document.getElementById('specificity-score');
    const techniqueAnalysisElem = document.getElementById('technique-analysis');
    const ambiguityPotentialElem = document.getElementById('ambiguity-potential');
    const improvementSuggestionsElem = document.getElementById('improvement-suggestions');
    const optimizedPromptElem = document.getElementById('optimized-prompt');
    const copyButton = document.getElementById('copy-button');


    // === EVENT LISTENERS ===

    /**
     * Event listener utama untuk form submission
     */
    promptForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Mencegah form dari refresh halaman

        const promptText = promptInput.value.trim();
        const selectedModel = targetModelSelect.value;

        // --- DEBUGGING LOGS ---
        console.log("--- DEBUGGING: Tombol Analisis Ditekan ---");
        console.log("Prompt yang akan dikirim:", promptText);
        console.log("Model yang dipilih:", selectedModel);
        // -----------------------

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
            console.error("Error Catcher di main.js:", error); // Log error detail
            showError(error.message);
        } finally {
            setLoadingState(false);
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