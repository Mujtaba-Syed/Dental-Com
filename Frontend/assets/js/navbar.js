// Navbar functionality for Dental-Com
class NavbarManager {
    constructor() {
        this.cartCountElement = null;
        this.apiBaseUrl = '/api/cart/';
        this.csrfToken = this.getCSRFToken();
        this.init();
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    }

    async makeRequest(url, method = 'GET', data = null) {
        // Get access token from localStorage
        const accessToken = localStorage.getItem('access_token');
        console.log('🛒 [NAVBAR] Access token found:', accessToken ? 'Yes' : 'No');
        
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            },
            credentials: 'same-origin'
        };

        // Add authorization header if token exists
        if (accessToken) {
            options.headers['Authorization'] = `Bearer ${accessToken}`;
            console.log('🛒 [NAVBAR] Authorization header added');
        } else {
            console.warn('🛒 [NAVBAR] No access token found, request may fail');
        }

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        console.log('🛒 [NAVBAR] Making request with options:', options);

        try {
            const response = await fetch(url, options);
            console.log('🛒 [NAVBAR] Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('🛒 [NAVBAR] HTTP Error Response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('🛒 [NAVBAR] API request failed:', error);
            throw error;
        }
    }

    // Initialize navbar functionality
    init() {
        console.log('🛒 [NAVBAR] Initializing navbar manager...');
        this.setupCartCountElement();
        this.loadCartCount();
        this.setupCartCountStyles();
        console.log('🛒 [NAVBAR] Navbar manager initialized successfully');
    }

    // Setup cart count element
    setupCartCountElement() {
        const cartIcon = document.querySelector('.shopping-cart');
        if (!cartIcon) {
            console.warn('🛒 [NAVBAR] Cart icon not found!');
            return;
        }

        // Create cart count badge
        this.cartCountElement = document.createElement('span');
        this.cartCountElement.className = 'cart-count-badge';
        this.cartCountElement.textContent = '0';
        
        // Make cart icon position relative for absolute positioning of badge
        cartIcon.style.position = 'relative';
        cartIcon.appendChild(this.cartCountElement);
        
        console.log('🛒 [NAVBAR] Cart count element created and attached');
    }

    // Setup cart count styles
    setupCartCountStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .cart-count-badge {
                position: absolute;
                top: -8px;
                right: -8px;
                background: #ff4757;
                color: white;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                font-size: 12px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                line-height: 1;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                z-index: 1000;
            }
            
            .cart-count-badge.hidden {
                display: none;
            }
            
            .cart-count-badge.animate {
                transform: scale(1.2);
                animation: cartBounce 0.3s ease-in-out;
            }
            
            @keyframes cartBounce {
                0% { transform: scale(1); }
                50% { transform: scale(1.3); }
                100% { transform: scale(1.2); }
            }
            
            .shopping-cart {
                position: relative !important;
            }
        `;
        document.head.appendChild(style);
        console.log('🛒 [NAVBAR] Cart count styles added');
    }

    // Load cart count from API
    async loadCartCount() {
        try {
            console.log('🛒 [NAVBAR] Loading cart count from API...');
            
            // Check if user is authenticated before making request
            const accessToken = localStorage.getItem('access_token');
            if (!accessToken) {
                console.log('🛒 [NAVBAR] User not authenticated, setting cart count to 0');
                this.updateCartCount(0);
                return;
            }
            
            const response = await this.makeRequest(`${this.apiBaseUrl}item-count/`);
            console.log('🛒 [NAVBAR] Cart count API response:', response);
            
            const count = response.total_quantity || 0;
            this.updateCartCount(count);
            
            console.log('🛒 [NAVBAR] Cart count loaded successfully:', count);
            
        } catch (error) {
            console.error('🛒 [NAVBAR] Failed to load cart count:', error);
            
            // If it's a 401 error, user is not authenticated
            if (error.message.includes('401')) {
                console.log('🛒 [NAVBAR] User not authenticated (401), setting cart count to 0');
            }
            
            this.updateCartCount(0);
        }
    }

    // Update cart count display
    updateCartCount(count) {
        if (!this.cartCountElement) {
            console.warn('🛒 [NAVBAR] Cart count element not found!');
            return;
        }

        console.log('🛒 [NAVBAR] Updating cart count display to:', count);
        
        // Update count text
        this.cartCountElement.textContent = count;
        
        // Show/hide badge based on count
        if (count > 0) {
            this.cartCountElement.classList.remove('hidden');
            // Add animation for new items
            this.cartCountElement.classList.add('animate');
            setTimeout(() => {
                this.cartCountElement.classList.remove('animate');
            }, 300);
        } else {
            this.cartCountElement.classList.add('hidden');
        }
        
        console.log('🛒 [NAVBAR] Cart count display updated');
    }

    // Refresh cart count (public method)
    async refreshCartCount() {
        console.log('🛒 [NAVBAR] Refreshing cart count...');
        await this.loadCartCount();
    }
    
    // Check authentication status and refresh cart count
    checkAuthAndRefreshCart() {
        console.log('🛒 [NAVBAR] Checking authentication and refreshing cart...');
        const accessToken = localStorage.getItem('access_token');
        console.log('🛒 [NAVBAR] Current auth status:', accessToken ? 'Authenticated' : 'Not authenticated');
        this.refreshCartCount();
    }

    // Get current cart count (public method)
    getCurrentCount() {
        if (!this.cartCountElement) return 0;
        return parseInt(this.cartCountElement.textContent) || 0;
    }
}

// Initialize navbar manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.navbarManager = new NavbarManager();
    console.log('🛒 [NAVBAR] Navbar manager created and available globally');
});

// Global function to refresh cart count (for use by other scripts)
window.refreshCartCount = function() {
    if (window.navbarManager) {
        window.navbarManager.refreshCartCount();
    }
};

// Global function to update cart count directly
window.updateCartCount = function(count) {
    if (window.navbarManager) {
        window.navbarManager.updateCartCount(count);
    }
};

// Global function to check auth and refresh cart
window.checkAuthAndRefreshCart = function() {
    if (window.navbarManager) {
        window.navbarManager.checkAuthAndRefreshCart();
    }
};

// Listen for storage changes to detect login/logout
window.addEventListener('storage', function(e) {
    if (e.key === 'access_token') {
        console.log('🛒 [NAVBAR] Access token changed, refreshing cart count...');
        if (window.navbarManager) {
            window.navbarManager.refreshCartCount();
        }
    }
});