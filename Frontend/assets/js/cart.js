// Cart functionality for Dental-Com
class CartManager {
    constructor() {
        this.apiBaseUrl = '/api/cart/';
        this.csrfToken = this.getCSRFToken();
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
        const accessToken = localStorage.getItem('access_token');
        console.log('🛒 [CART] Access token found:', accessToken ? 'Yes' : 'No', accessToken);
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.csrfToken,
            'Authorization': `Bearer ${accessToken}`,
        };
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }
        const options = {
            method: method,
            headers: headers,
            credentials: 'same-origin'
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Fetch cart data
    async fetchCart() {
        try {
            const cartData = await this.makeRequest(this.apiBaseUrl);
            return cartData;
        } catch (error) {
            console.error('Failed to fetch cart:', error);
            return null;
        }
    }

    // Increase item quantity
    async increaseQuantity(cartItemId) {
        try {
            const result = await this.makeRequest(
                `${this.apiBaseUrl}increase/${cartItemId}/`,
                'POST'
            );
            return result;
        } catch (error) {
            console.error('Failed to increase quantity:', error);
            throw error;
        }
    }

    // Decrease item quantity
    async decreaseQuantity(cartItemId) {
        try {
            const result = await this.makeRequest(
                `${this.apiBaseUrl}decrease/${cartItemId}/`,
                'POST'
            );
            return result;
        } catch (error) {
            console.error('Failed to decrease quantity:', error);
            throw error;
        }
    }

    // Remove item from cart
    async removeItem(cartItemId) {
        try {
            const result = await this.makeRequest(
                `${this.apiBaseUrl}remove/${cartItemId}/`,
                'DELETE'
            );
            return result;
        } catch (error) {
            console.error('Failed to remove item:', error);
            throw error;
        }
    }

    // Update cart display
    updateCartDisplay(cartData) {
        if (!cartData || !cartData.items) {
            this.showEmptyCart();
            return;
        }

        this.renderCartItems(cartData.items);
        this.updateCartTotals(cartData);
        
        // Update navbar cart count
        this.updateNavbarCartCount(cartData.total_items || 0);
    }

    // Render cart items
    renderCartItems(items) {
        const tbody = document.querySelector('.cart-table tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        items.forEach(item => {
            const row = this.createCartItemRow(item);
            tbody.appendChild(row);
        });
    }

// Create cart item row
createCartItemRow(item) {
    const row = document.createElement('tr');
    row.className = 'table-body-row';
    row.setAttribute('data-cart-item-id', item.id);

    const primaryImage = item.product.images.find(img => img.is_primary) || item.product.images[0];
    const imageUrl = primaryImage ? primaryImage.image : '/static/img/products/product-img-1.jpg';

    row.innerHTML = `
        <td class="product-remove">
            <a href="#" onclick="cartManager.removeItemHandler(${item.id})">
                <i class="far fa-window-close"></i>
            </a>
        </td>
        <td class="product-image" style="padding: 0; margin: 0;">
            <img 
                src="${imageUrl}" 
                alt="${item.product.name}"
                style="
                    width: 400px;
                    height: 200px;
                    object-fit: contain;
                    display: block;
                    margin: 0;
                    padding: 0;
                    background-color: transparent;
                    border-radius: 0;
                "
            >
        </td>
        <td class="product-name">${item.product.name}</td>
        <td class="product-price">Rs ${item.product.current_price}</td>
        <td class="product-quantity">
            <div class="quantity-controls">
                <button type="button" class="quantity-btn minus" onclick="cartManager.decreaseQuantityHandler(${item.id})">-</button>
                <input type="number" value="${item.quantity}" min="1" readonly>
                <button type="button" class="quantity-btn plus" onclick="cartManager.increaseQuantityHandler(${item.id})">+</button>
            </div>
        </td>
        <td class="product-total">Rs ${item.total_price}</td>
    `;

    return row;
}


    // Update cart totals
    updateCartTotals(cartData) {
        const subtotalElement = document.querySelector('.total-data:nth-child(1) td:last-child');
        const totalElement = document.querySelector('.total-data:nth-child(3) td:last-child');

        if (subtotalElement) {
            subtotalElement.textContent = `Rs ${cartData.total_price}`;
        }

        if (totalElement) {
            // Assuming shipping is fixed at Rs 45
            const shipping = 45;
            const total = cartData.total_price + shipping;
            totalElement.textContent = `Rs ${total}`;
        }

        // Update shipping display
        const shippingElement = document.querySelector('.total-data:nth-child(2) td:last-child');
        if (shippingElement) {
            shippingElement.textContent = 'Rs 45';
        }
    }

    // Show empty cart message
    showEmptyCart() {
        const tbody = document.querySelector('.cart-table tbody');
        if (!tbody) return;

        tbody.innerHTML = `
            <tr class="table-body-row">
                <td colspan="6" class="text-center" style="padding: 50px;">
                    <h4>Your cart is empty</h4>
                    <p>Add some products to get started!</p>
                    <a href="/shop.html" class="boxed-btn">Continue Shopping</a>
                </td>
            </tr>
        `;

        // Update totals to zero
        this.updateCartTotals({ total_price: 0, total_items: 0 });
        
        // Update navbar cart count to zero
        this.updateNavbarCartCount(0);
    }
    
    // Update navbar cart count
    updateNavbarCartCount(count) {
        console.log('🛒 [CART] Updating navbar cart count to:', count);
        
        if (window.updateCartCount) {
            window.updateCartCount(count);
            console.log('🛒 [CART] Navbar cart count updated successfully');
        } else {
            console.warn('🛒 [CART] Navbar manager not available for cart count update');
        }
    }

    // Event handlers
    async increaseQuantityHandler(cartItemId) {
        try {
            const result = await this.increaseQuantity(cartItemId);
            this.updateCartDisplay(result.cart);
            this.showNotification('Quantity increased', 'success');
        } catch (error) {
            this.showNotification('Failed to increase quantity', 'error');
        }
    }

    async decreaseQuantityHandler(cartItemId) {
        try {
            const result = await this.decreaseQuantity(cartItemId);
            this.updateCartDisplay(result.cart);
            this.showNotification(result.message, 'success');
        } catch (error) {
            this.showNotification('Failed to decrease quantity', 'error');
        }
    }

    async removeItemHandler(cartItemId) {
        if (confirm('Are you sure you want to remove this item from your cart?')) {
            try {
                const result = await this.removeItem(cartItemId);
                this.updateCartDisplay(result.cart);
                this.showNotification('Item removed from cart', 'success');
            } catch (error) {
                this.showNotification('Failed to remove item', 'error');
            }
        }
    }

    // Show notification
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            z-index: 9999;
            transition: all 0.3s ease;
        `;

        // Set background color based on type
        switch (type) {
            case 'success':
                notification.style.backgroundColor = '#28a745';
                break;
            case 'error':
                notification.style.backgroundColor = '#dc3545';
                break;
            default:
                notification.style.backgroundColor = '#17a2b8';
        }

        document.body.appendChild(notification);

        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // Initialize cart
    async init() {
        try {
            const cartData = await this.fetchCart();
            this.updateCartDisplay(cartData);
        } catch (error) {
            console.error('Failed to initialize cart:', error);
            this.showEmptyCart();
        }
    }
}

// Initialize cart manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.cartManager = new CartManager();
    cartManager.init();
});

// Add CSS for quantity controls
const style = document.createElement('style');
style.textContent = `
    .quantity-controls {
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .quantity-btn {
        width: 30px;
        height: 30px;
        border: 1px solid #ddd;
        background: #f8f9fa;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    
    .quantity-btn:hover {
        background: #e9ecef;
        border-color: #adb5bd;
    }
    
    .quantity-btn:active {
        background: #dee2e6;
    }
    
    .quantity-controls input {
        width: 60px;
        text-align: center;
        border: 1px solid #ddd;
        padding: 5px;
        background: white;
    }
    
    .quantity-controls input:focus {
        outline: none;
        border-color: #007bff;
    }
`;
document.head.appendChild(style);