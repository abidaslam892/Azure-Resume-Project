/**
 * Simple Real Visitor Counter with Better Error Handling
 */

class VisitorCounter {
    constructor() {
        this.apiUrl = 'https://func-resume-1760986821.azurewebsites.net/api/visitor-counter';
        this.countElement = document.getElementById('visitor-count');
        this.init();
    }

    async init() {
        console.log('🔄 Starting visitor counter...');
        this.showLoading();
        
        // Clear any localStorage
        try {
            localStorage.removeItem('resume_visitor_count');
        } catch (e) {
            console.log('localStorage not available');
        }
        
        // Try to get real count
        try {
            console.log('🌐 Calling API:', this.apiUrl);
            const count = await this.getCount();
            console.log('✅ API Success, count:', count);
            this.displayCount(count);
            this.showSuccess();
        } catch (error) {
            console.error('❌ API Failed:', error.message);
            console.error('Full error:', error);
            this.showError(error.message);
        }
    }

    async getCount() {
        console.log('📡 Making API request...');
        
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors'
        });

        console.log('📡 Response status:', response.status);
        console.log('📡 Response ok:', response.ok);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('📊 Response data:', data);

        if (!data.success || typeof data.count !== 'number') {
            throw new Error('Invalid API response format');
        }

        return data.count;
    }

    displayCount(count) {
        if (!this.countElement) {
            console.error('❌ visitor-count element not found');
            return;
        }
        this.countElement.textContent = count.toLocaleString();
    }

    showLoading() {
        if (this.countElement) {
            this.countElement.textContent = 'Loading...';
            this.countElement.style.color = '#6b7280';
        }
    }

    showSuccess() {
        if (this.countElement) {
            this.countElement.style.color = '#10b981';
            this.countElement.style.textShadow = '0 0 8px rgba(34, 197, 94, 0.5)';
            console.log('💚 Success - showing real count');
        }
    }

    showError(errorMsg) {
        if (this.countElement) {
            this.countElement.textContent = `Error: ${errorMsg}`;
            this.countElement.style.color = '#ef4444';
            console.log('❌ Error displayed to user');
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM loaded, initializing counter...');
    new VisitorCounter();
});

// Backup initialization
setTimeout(() => {
    if (document.getElementById('visitor-count')) {
        console.log('🔄 Backup initialization...');
        new VisitorCounter();
    }
}, 2000);

console.log('📄 Simple visitor counter script loaded');