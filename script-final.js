/**
 * Real Visitor Counter for Cloud Resume Challenge
 * Azure Storage Tables via Azure Function API
 */

class VisitorCounter {
    constructor() {
        this.apiUrl = 'https://func-resume-1760986821.azurewebsites.net/api/visitor-counter';
        this.countElement = document.getElementById('visitor-count');
        this.init();
    }

    async init() {
        console.log('🔄 Initializing real visitor counter...');
        this.showLoading();
        
        try {
            const count = await this.incrementVisitorCount();
            console.log('✅ Got real count from Azure Storage Tables:', count);
            this.displayCount(count);
            this.showSuccess();
        } catch (error) {
            console.error('❌ API Error:', error.message);
            this.showError();
        }
    }

    async incrementVisitorCount() {
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        
        if (!data.success || typeof data.count !== 'number') {
            throw new Error('Invalid API response');
        }

        return data.count;
    }

    displayCount(count) {
        if (!this.countElement) return;
        
        // Animate counter
        this.animateCounter(0, count);
    }

    animateCounter(start, end) {
        const duration = 1500;
        const startTime = performance.now();
        
        const update = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (end - start) * progress);
            
            this.countElement.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        };
        
        requestAnimationFrame(update);
    }

    showLoading() {
        if (this.countElement) {
            this.countElement.textContent = 'Loading...';
            this.countElement.style.color = '#6b7280';
        }
    }

    showSuccess() {
        if (this.countElement) {
            // Green styling for real data
            this.countElement.style.color = '#10b981';
            this.countElement.style.textShadow = '0 0 8px rgba(34, 197, 94, 0.6)';
            
            // Clear shadow after 3 seconds
            setTimeout(() => {
                this.countElement.style.textShadow = '';
            }, 3000);
        }
    }

    showError() {
        if (this.countElement) {
            this.countElement.textContent = 'API Error';
            this.countElement.style.color = '#ef4444';
        }
    }
}

// Initialize when ready
function initCounter() {
    const element = document.getElementById('visitor-count');
    if (element) {
        new VisitorCounter();
    } else {
        // Try again in 100ms
        setTimeout(initCounter, 100);
    }
}

// Start initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCounter);
} else {
    initCounter();
}

console.log('📄 Real visitor counter loaded - Azure Storage Tables');