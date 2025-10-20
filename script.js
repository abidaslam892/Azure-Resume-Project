/**
 * Professional Visitor Counter Script - Azure Resume Project
 * 
 * This script provides a robust visitor counter implementation with:
 * - Comprehensive error handling and retry logic
 * - Professional logging and debugging capabilities  
 * - Modern ES6+ JavaScript features
 * - Accessibility and user experience optimization
 * - Enterprise-grade API integration patterns
 * 
 * @author Abid Aslam
 * @version 2.0.0
 * @license MIT
 */

class VisitorCounter {
    constructor() {
        // Configuration
        this.apiUrl = 'https://func-resume-1760986821.azurewebsites.net/api/visitor-counter';
        this.countElement = document.getElementById('visitor-count');
        this.retryAttempts = 3;
        this.retryDelay = 1000; // 1 second
        this.timeout = 10000; // 10 seconds
        
        // State management
        this.isLoading = false;
        this.hasError = false;
        this.currentCount = 0;
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    /**
     * Initialize the visitor counter
     */
    async init() {
        try {
            await this.updateVisitorCount();
            this.setupErrorHandling();
        } catch (error) {
            console.error('Failed to initialize visitor counter:', error);
            this.showError();
        }
    }

    /**
     * Fetch and update the visitor count from Azure Function
     */
    async updateVisitorCount() {
        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                const response = await this.fetchWithTimeout(this.apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        action: 'increment'
                    })
                }, 5000); // 5 second timeout

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                if (data && typeof data.count === 'number') {
                    this.displayCount(data.count);
                    this.showSuccess();
                    return;
                } else {
                    throw new Error('Invalid response format');
                }

            } catch (error) {
                console.warn(`Attempt ${attempt} failed:`, error.message);
                
                if (attempt === this.retryAttempts) {
                    throw error;
                }
                
                await this.delay(this.retryDelay * attempt);
            }
        }
    }

    /**
     * Fetch with timeout wrapper
     */
    async fetchWithTimeout(url, options, timeout) {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(id);
            return response;
        } catch (error) {
            clearTimeout(id);
            throw error;
        }
    }

    /**
     * Display the visitor count with animation
     */
    displayCount(count) {
        if (!this.countElement) return;

        // Animate the counter
        this.animateCounter(count);
    }

    /**
     * Animate the counter from 0 to the target count
     */
    animateCounter(targetCount) {
        const duration = 1500; // 1.5 seconds
        const startTime = performance.now();
        const startCount = 0;

        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentCount = Math.floor(startCount + (targetCount - startCount) * easeOut);
            
            this.countElement.textContent = this.formatNumber(currentCount);
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                this.countElement.textContent = this.formatNumber(targetCount);
            }
        };

        requestAnimationFrame(updateCounter);
    }

    /**
     * Format number with commas for better readability
     */
    formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    /**
     * Show success state
     */
    showSuccess() {
        if (!this.countElement) return;
        
        this.countElement.classList.remove('error', 'loading');
        this.countElement.classList.add('success');
        
        // Add a subtle glow effect
        this.countElement.style.textShadow = '0 0 10px rgba(102, 126, 234, 0.5)';
        setTimeout(() => {
            this.countElement.style.textShadow = '';
        }, 2000);
    }

    /**
     * Show error state
     */
    showError() {
        if (!this.countElement) return;
        
        this.countElement.classList.remove('success', 'loading');
        this.countElement.classList.add('error');
        this.countElement.textContent = 'N/A';
        
        // Show tooltip or fallback message
        this.countElement.title = 'Unable to load visitor count. Please try refreshing the page.';
    }

    /**
     * Show loading state
     */
    showLoading() {
        if (!this.countElement) return;
        
        this.countElement.classList.add('loading');
        this.countElement.textContent = 'Loading...';
    }

    /**
     * Setup error handling for network issues
     */
    setupErrorHandling() {
        window.addEventListener('online', () => {
            console.log('Connection restored, retrying visitor count...');
            this.init();
        });

        window.addEventListener('offline', () => {
            console.log('Connection lost');
            this.showError();
        });
    }

    /**
     * Utility function to delay execution
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Get visitor count without incrementing (for analytics)
     */
    async getVisitorCount() {
        try {
            const response = await this.fetchWithTimeout(this.apiUrl, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            }, 5000);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.count;
        } catch (error) {
            console.error('Failed to get visitor count:', error);
            return null;
        }
    }
}

/**
 * Analytics and tracking utilities
 */
class Analytics {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.startTime = Date.now();
    }

    /**
     * Generate a unique session ID
     */
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    /**
     * Track page view duration
     */
    trackPageView() {
        const duration = Date.now() - this.startTime;
        
        // Track engagement (time spent on page)
        window.addEventListener('beforeunload', () => {
            const totalDuration = Date.now() - this.startTime;
            
            // Send analytics data (if needed)
            console.log('Page view duration:', totalDuration, 'ms');
            
            // You could send this to Azure Application Insights or other analytics service
            this.sendAnalytics({
                event: 'page_view',
                duration: totalDuration,
                sessionId: this.sessionId,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            });
        });
    }

    /**
     * Send analytics data to backend (optional)
     */
    async sendAnalytics(data) {
        try {
            // This could be sent to Azure Application Insights
            console.log('Analytics data:', data);
            
            // Example: Send to Azure Function for logging
            // await fetch('/api/analytics', {
            //     method: 'POST',
            //     headers: { 'Content-Type': 'application/json' },
            //     body: JSON.stringify(data)
            // });
        } catch (error) {
            console.error('Failed to send analytics:', error);
        }
    }
}

/**
 * Page interaction enhancements
 */
class InteractionEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.setupSmoothScrolling();
        this.setupLazyLoading();
        this.setupAccessibility();
    }

    /**
     * Setup smooth scrolling for anchor links
     */
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Setup lazy loading for images
     */
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * Setup accessibility improvements
     */
    setupAccessibility() {
        // Add keyboard navigation for interactive elements
        document.querySelectorAll('.skill-tag, .cert-item, .project-item').forEach(element => {
            element.setAttribute('tabindex', '0');
            
            element.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    element.click();
                }
            });
        });

        // Add focus indicators
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }
}

/**
 * Initialize everything when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize visitor counter
    const visitorCounter = new VisitorCounter();
    
    // Initialize analytics
    const analytics = new Analytics();
    analytics.trackPageView();
    
    // Initialize interaction enhancements
    const enhancer = new InteractionEnhancer();
    
    // Add performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log('Page load time:', loadTime, 'ms');
        });
    }
    
    // Add error tracking
    window.addEventListener('error', (e) => {
        console.error('JavaScript error:', e.error);
    });
    
    // Add unhandled promise rejection tracking
    window.addEventListener('unhandledrejection', (e) => {
        console.error('Unhandled promise rejection:', e.reason);
    });
});

/**
 * Add CSS for enhanced states
 */
const style = document.createElement('style');
style.textContent = `
    .counter-number.loading {
        opacity: 0.6;
        animation: pulse 1.5s infinite;
    }
    
    .counter-number.error {
        color: #e53e3e !important;
        opacity: 0.8;
    }
    
    .counter-number.success {
        color: #38a169 !important;
    }
    
    .keyboard-navigation *:focus {
        outline: 2px solid #667eea !important;
        outline-offset: 2px !important;
    }
    
    img.lazy {
        filter: blur(5px);
        transition: filter 0.3s;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
`;
document.head.appendChild(style);