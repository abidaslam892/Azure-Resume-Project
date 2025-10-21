/**
 * Simple Visitor Counter for Cloud Resume Challenge
 * Robust implementation with fallback support
 */

class VisitorCounter {
    constructor() {
        this.apiUrl = 'https://func-resume-1760986821.azurewebsites.net/api/visitor-counter';
        this.countElement = document.getElementById('visitor-count');
        this.storageKey = 'resume_visitor_count';
        this.init();
    }

    async init() {
        console.log('🔄 Initializing visitor counter...');
        this.showLoading();
        
        // Clear any existing localStorage data to start fresh with real API
        this.clearFallbackData();
        
        try {
            // Try to get count from Azure Function first
            const count = await this.getCountFromAPI();
            if (count !== null) {
                console.log('✅ Got REAL count from Azure Storage Tables:', count);
                this.displayCount(count);
                this.showSuccess('real');
                return;
            }
        } catch (error) {
            console.warn('⚠️ Azure Function not available, will show error:', error.message);
            this.showError();
        }
    }

    clearFallbackData() {
        // Remove any stored localStorage count to start fresh
        localStorage.removeItem(this.storageKey);
        console.log('�️ Cleared localStorage fallback data');
    }

    async getCountFromAPI() {
        try {
            console.log('🌐 Attempting to connect to Azure Function...');
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000); // 8 second timeout
            
            // First, try to increment the count with a POST request
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
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
                console.log('✅ Successfully retrieved count from Azure Storage Tables:', data.count);
                return data.count;
            } else {
                throw new Error('Invalid response format from API');
            }
            
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('API request timed out');
            }
            console.error('❌ API Error:', error);
            throw error;
        }
    }

    getFallbackCount() {
        // Get or create realistic visitor count
        let count = localStorage.getItem(this.storageKey);
        
        if (!count) {
            // Initialize with a realistic base count
            const baseCount = 1247; // Realistic starting number
            const todayBonus = Math.floor(Math.random() * 15) + 5; // 5-20 visits today
            count = baseCount + todayBonus;
            localStorage.setItem(this.storageKey, count.toString());
            console.log(`🆕 Initialized visitor count: ${count}`);
        } else {
            // Increment for this visit
            count = parseInt(count) + 1;
            localStorage.setItem(this.storageKey, count.toString());
            console.log(`⬆️ Incremented visitor count: ${count}`);
        }
        
        return count;
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
        }
    }

    showSuccess(source = 'unknown') {
        if (this.countElement) {
            this.countElement.className = 'visitor-number success';
            
            // Add different effects based on data source
            if (source === 'real') {
                // Green glow for real data
                this.countElement.style.textShadow = '0 0 8px rgba(34, 197, 94, 0.8)';
                console.log('💚 Displaying REAL visitor count from Azure Storage Tables');
            } else if (source === 'fallback') {
                // Blue glow for fallback data
                this.countElement.style.textShadow = '0 0 8px rgba(125, 211, 252, 0.6)';
                console.log('💙 Displaying FALLBACK visitor count from localStorage');
            }
            
            setTimeout(() => {
                this.countElement.style.textShadow = '';
            }, 3000);
        }
    }

    showError() {
        if (this.countElement) {
            this.countElement.textContent = 'API Error';
            this.countElement.className = 'visitor-number error';
            this.countElement.style.color = '#ef4444';
            console.log('❌ Displaying error - Azure Function not available');
        }
    }
}

// Initialize when DOM is ready
function initVisitorCounter() {
    console.log('🚀 Starting visitor counter initialization...');
    
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

console.log('📄 Visitor counter script loaded');