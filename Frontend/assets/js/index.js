// index page js Here

// Product data and cart functionality
let products = [];
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    initializeCartButtons();
    updateCartDisplay();
});

// Load products from API
async function loadProducts() {
    try {
        const response = await fetch('/api/products/');
        const data = await response.json();
        products = data.results;
        console.log('Products loaded:', products);
        
        // Debug: Check image URLs
        products.forEach(product => {
            console.log(`Product: ${product.name}`);
            console.log(`Primary Image:`, product.primary_image);
            if (product.primary_image) {
                console.log(`Image URL: ${product.primary_image.image}`);
                // Test if image loads
                const img = new Image();
                img.onload = () => console.log(`Image loaded successfully: ${product.primary_image.image}`);
                img.onerror = () => console.error(`Image failed to load: ${product.primary_image.image}`);
                img.src = product.primary_image.image;
            }
        });
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Initialize cart buttons
function initializeCartButtons() {
    const cartButtons = document.querySelectorAll('.cart-btn');
    cartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });
}

// Add product to cart
function addToCart(productId) {
    const product = products.find(p => p.id == productId);
    if (!product) {
        console.error('Product not found:', productId);
        return;
    }

    const existingItem = cart.find(item => item.id == productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: parseFloat(product.price),
            image: product.primary_image ? product.primary_image.image : '/static/img/products/default.jpg',
            quantity: 1
        });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDisplay();
    showCartNotification(product.name);
}

// Update cart display
function updateCartDisplay() {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
    }
}

// Show cart notification
function showCartNotification(productName) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-check-circle"></i>
            <span>${productName} added to cart!</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .notification-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Product search functionality
function searchProducts(query) {
    const productItems = document.querySelectorAll('.single-product-item');
    productItems.forEach(item => {
        const productName = item.querySelector('h3').textContent.toLowerCase();
        const productDescription = item.querySelector('.product-price').textContent.toLowerCase();
        
        if (productName.includes(query.toLowerCase()) || productDescription.includes(query.toLowerCase())) {
            item.closest('.col-lg-4').style.display = 'block';
        } else {
            item.closest('.col-lg-4').style.display = 'none';
        }
    });
}

// Filter products by category
function filterProducts(category) {
    const productItems = document.querySelectorAll('.single-product-item');
    productItems.forEach(item => {
        const productCategory = item.getAttribute('data-category');
        if (category === 'all' || productCategory === category) {
            item.closest('.col-lg-4').style.display = 'block';
        } else {
            item.closest('.col-lg-4').style.display = 'none';
        }
    });
}

// Smooth scrolling for anchor links
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

// Initialize tooltips if Bootstrap is available
if (typeof bootstrap !== 'undefined') {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
} 