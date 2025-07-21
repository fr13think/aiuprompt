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
    }
};