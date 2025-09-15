// index page js Here

// Product data and cart functionality
let products = [];
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadServices();
    initializeBookingButtons();
    updateCartDisplay();
});

// Load services from API
async function loadServices() {
    try {
        const response = await fetch('/api/services/');
        const data = await response.json();
        products = data.results; // Keep using 'products' variable for compatibility
        console.log('Services loaded:', products);
        
        // Debug: Check image URLs
        products.forEach(service => {
            console.log(`Service: ${service.name}`);
            console.log(`Image:`, service.image);
            if (service.image) {
                console.log(`Image URL: ${service.image}`);
                // Test if image loads
                const img = new Image();
                img.onload = () => console.log(`Image loaded successfully: ${service.image}`);
                img.onerror = () => console.error(`Image failed to load: ${service.image}`);
                img.src = service.image;
            }
        });
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

// Initialize booking buttons
function initializeBookingButtons() {
    const bookingButtons = document.querySelectorAll('.cart-btn');
    bookingButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const serviceId = this.getAttribute('data-service-id');
            if (serviceId) {
                handleServiceBooking(serviceId);
            }
        });
    });
}

// Handle service booking
function handleServiceBooking(serviceId) {
    const service = products.find(s => s.id == serviceId);
    if (!service) {
        console.error('Service not found:', serviceId);
        return;
    }

    // Store selected service for appointment booking
    localStorage.setItem('selectedService', JSON.stringify({
        id: service.id,
        name: service.name,
        description: service.description
    }));

    // Show booking notification
    showBookingNotification(service.name);
}

// Update cart display
function updateCartDisplay() {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
    }
}

// Show booking notification
function showBookingNotification(serviceName) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'booking-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-calendar-check"></i>
            <span>Redirecting to book ${serviceName} appointment...</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #007bff;
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
    
    // Remove notification after 2 seconds and redirect
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            // Redirect to contact page after notification
            window.location.href = '/contact/';
        }, 300);
    }, 2000);
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