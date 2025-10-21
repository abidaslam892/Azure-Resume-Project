/**
 * Real-Only Visitor Counter for Cloud Resume Challenge
 * No fallback - uses only Azure Storage Tables via Azure Function API
 */

class VisitorCounter {
    constructor() {
        this.apiUrl = 'https://func-resume-1760986821.azurewebsites.net/api/visitor-counter';
        this.countElement = document.getElementById('visitor-count');
        this.storageKey = 'resume_visitor_count';
        this.init();
    }

    async init() {
        console.log('🔄 Initializing REAL visitor counter (Azure Storage Tables only)...');
        this.showLoading();
        
        // Clear any existing localStorage data
        this.clearFallbackData();
        
        try {
            // Get count from Azure Function API (increment visitor)
            const count = await this.getCountFromAPI();
            if (count !== null) {
                console.log('✅ Got REAL count from Azure Storage Tables:', count);
                this.displayCount(count);
                this.showSuccess();
                return;
            }
        } catch (error) {
            console.error('❌ Azure Function not available:', error.message);
            this.showError();
        }
    }

    async getCountFromAPI() {
        try {
            console.log('🌐 Connecting to Azure Function API...');
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
            
            // Increment the count with a POST request (new visitor)
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache',
                },
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('📊 API Response:', data);
            
            if (data && data.success && typeof data.count === 'number') {
                console.log('✅ Successfully retrieved real count from Azure Storage Tables:', data.count);
                console.log('📈 Visitor count incremented to:', data.count);
                return data.count;
            } else {
                throw new Error('Invalid response format from API');
            }
            
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('API request timed out after 10 seconds');
            }
            console.error('❌ API Error:', error);
            throw error;
        }
    }

    clearFallbackData() {
        // Remove any stored localStorage count to start fresh
        try {
            localStorage.removeItem(this.storageKey);
            // Also clear any other potential storage keys
            localStorage.removeItem('visitor_count');
            localStorage.removeItem('resume_visitors');
            console.log('🗑️ Cleared all localStorage fallback data');
        } catch (e) {
            console.log('🗑️ localStorage not available or already clear');
        }
    }

    displayCount(count) {
        if (!this.countElement) {
            console.error('❌ visitor-count element not found');
            return;
        }
        
        // Animate the counter
        this.animateCounter(count);
    }

    animateCounter(targetCount) {
        const duration = 2000; // 2 seconds
        const startTime = performance.now();
        const startCount = 0;
        
        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Smooth easing function
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentCount = Math.floor(startCount + (targetCount - startCount) * easeOut);
            
            this.countElement.textContent = this.formatNumber(currentCount);
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                this.countElement.textContent = this.formatNumber(targetCount);
                console.log(`🎯 Counter animation completed: ${targetCount}`);
            }
        };
        
        requestAnimationFrame(updateCounter);
    }

    formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    showLoading() {
        if (this.countElement) {
            this.countElement.textContent = 'Loading...';
            this.countElement.className = 'visitor-number loading';
            this.countElement.style.color = '#6b7280';
        }
    }

    showSuccess() {
        if (this.countElement) {
            this.countElement.className = 'visitor-number success';
            
            // Green glow for real data from Azure Storage Tables
            this.countElement.style.textShadow = '0 0 8px rgba(34, 197, 94, 0.8)';
            this.countElement.style.color = '#10b981';
            console.log('💚 Displaying REAL visitor count from Azure Storage Tables');
            
            setTimeout(() => {
                this.countElement.style.textShadow = '';
                this.countElement.style.color = '';
            }, 3000);
        }
    }

    showError() {
        if (this.countElement) {
            this.countElement.textContent = 'API Unavailable';
            this.countElement.className = 'visitor-number error';
            this.countElement.style.color = '#ef4444';
            this.countElement.style.textShadow = '0 0 4px rgba(239, 68, 68, 0.4)';
            console.log('❌ Azure Function API not available - showing error');
        }
    }
}

// Initialize when DOM is ready
function initVisitorCounter() {
    console.log('🚀 Starting REAL-ONLY visitor counter initialization...');
    
    // Wait for the visitor-count element to be available
    const checkElement = () => {
        const element = document.getElementById('visitor-count');
        if (element) {
            console.log('✅ Found visitor-count element');
            new VisitorCounter();
        } else {
            console.log('⏳ Waiting for visitor-count element...');
            setTimeout(checkElement, 100);
        }
    };
    
    checkElement();
}

// Multiple initialization strategies
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initVisitorCounter);
} else {
    initVisitorCounter();
}

// Backup initialization
setTimeout(initVisitorCounter, 1000);

// Global access for debugging
window.VisitorCounter = VisitorCounter;

console.log('📄 Real-only visitor counter script loaded - no localStorage fallback');