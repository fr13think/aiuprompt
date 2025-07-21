/**
 * Modul untuk berkomunikasi dengan API backend uprompt-ai.
 */
const api = {
    /**
     * Mengirimkan prompt ke backend untuk dianalisis.
     * @param {string} promptText - Teks prompt yang akan dianalisis.
     * @param {string} targetModel - Model AI yang ditargetkan (misal: 'default', 'gpt-4o').
     * @returns {Promise<object>} - Sebuah promise yang akan resolve dengan data hasil analisis.
     * @throws {Error} - Melemparkan error jika respons API tidak ok atau terjadi kesalahan jaringan.
     */
    async analyzePrompt(promptText, targetModel) {
        debugger;

        const API_URL = '/api/v1/analysis/';

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: promptText,
                target_model: targetModel // Pastikan variabel ini sama dengan nama parameter
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            const errorMessage = `Error ${response.status}: ${errorData.detail || response.statusText}`;
            throw new Error(errorMessage);
        }

        return response.json();
    },

    /**
     * Mengambil daftar template prompt dari backend.
     * @returns {Promise<Array>} - Sebuah promise yang akan resolve dengan array berisi template.
     * @throws {Error} - Melemparkan error jika gagal memuat template.
     */
    async getTemplates() {
        const API_URL = '/api/v1/templates/';
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('Gagal memuat template.');
        }
        return response.json();
    },

    // fungsi untuk register dan login
    async registerUser(email, password) {
        const response = await fetch('/api/v1/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Gagal mendaftar.');
        }
        return response.json();
    },

    async loginUser(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData,
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Gagal login.');
        }
        return response.json();
    },
};