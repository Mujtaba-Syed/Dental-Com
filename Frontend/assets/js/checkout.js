// Checkout page functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛒 [CHECKOUT] Initializing checkout page...');
    
    // Get DOM elements
    const orderDetailsBody = document.querySelector('.order-details-body');
    const checkoutDetails = document.querySelector('.checkout-details');
    const placeOrderBtn = document.querySelector('.boxed-btn');
    
    // Store cart data globally
    let cartData = null;
    
    // Check if user is authenticated
    function isAuthenticated() {
        const token = localStorage.getItem('access_token');
        return token !== null;
    }
    
    // Get access token
    function getAccessToken() {
        return localStorage.getItem('access_token');
    }
    
    // Fetch cart data from API
    async function fetchCartData() {
        try {
            console.log('🛒 [CHECKOUT] Fetching cart data...');
            
            if (!isAuthenticated()) {
                console.warn('🛒 [CHECKOUT] User not authenticated');
                showEmptyCart('Please login to view your cart');
                return null;
            }
            
            const accessToken = getAccessToken();
            const response = await fetch('/api/cart/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    console.error('🛒 [CHECKOUT] Unauthorized - User not authenticated');
                    showEmptyCart('Please login to view your cart');
                    return null;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const cartData = await response.json();
            console.log('🛒 [CHECKOUT] Cart data received:', cartData);
            
            // Store cart data globally
            window.cartData = cartData;
            return cartData;
            
        } catch (error) {
            console.error('🛒 [CHECKOUT] Error fetching cart data:', error);
            showError('Failed to load cart data');
            return null;
        }
    }
    
    // Display cart items
    function displayCartItems(cartData) {
        if (!cartData || !cartData.items || cartData.items.length === 0) {
            showEmptyCart('Your cart is empty');
            return;
        }
        
        console.log('🛒 [CHECKOUT] Displaying cart items...');
        
        // Clear existing content
        orderDetailsBody.innerHTML = '';
        
        // Add header row
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `
            <th>Product</th>
            <th>Details</th>
        `;
        orderDetailsBody.appendChild(headerRow);
        
        // Add each cart item
        cartData.items.forEach(item => {
            const product = item.product;
            const quantity = item.quantity;
            const unitPrice = product.current_price;
            const totalPrice = item.total_price;
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <strong>${product.name}</strong>
                </td>
                <td>
                    <div>Qty: ${quantity}</div>
                    <div>Unit: Rs ${unitPrice.toFixed(2)}</div>
                    <div><strong>Total: Rs ${totalPrice.toFixed(2)}</strong></div>
                </td>
            `;
            orderDetailsBody.appendChild(row);
        });
        
        // Update checkout details (subtotal, shipping, total)
        updateCheckoutDetails(cartData);
    }
    
    // Update checkout summary (subtotal, shipping, total)
    function updateCheckoutDetails(cartData) {
        if (!cartData) return;
        
        const subtotal = cartData.total_price;
        const shipping = 50; // Fixed shipping cost
        const total = subtotal + shipping;
        
        checkoutDetails.innerHTML = `
            <tr>
                <td>Subtotal</td>
                <td>Rs ${subtotal.toFixed(2)}</td>
            </tr>
            <tr>
                <td>Shipping</td>
                <td>Rs ${shipping.toFixed(2)}</td>
            </tr>
            <tr>
                <td><strong>Total</strong></td>
                <td><strong>Rs ${total.toFixed(2)}</strong></td>
            </tr>
        `;
        
        console.log('🛒 [CHECKOUT] Checkout details updated:', {
            subtotal,
            shipping,
            total
        });
    }
    
    // Show empty cart message
    function showEmptyCart(message) {
        console.log('🛒 [CHECKOUT] Showing empty cart message');
        
        orderDetailsBody.innerHTML = `
            <tr>
                <td colspan="2" style="text-align: center; padding: 20px;">
                    <p style="color: #666; font-size: 16px;">${message}</p>
                    <a href="/shop/" class="btn btn-primary" style="margin-top: 10px;">Continue Shopping</a>
                </td>
            </tr>
        `;
        
        checkoutDetails.innerHTML = `
            <tr>
                <td>Subtotal</td>
                <td>Rs 0.00</td>
            </tr>
            <tr>
                <td>Shipping</td>
                <td>Rs 0.00</td>
            </tr>
            <tr>
                <td><strong>Total</strong></td>
                <td><strong>Rs 0.00</strong></td>
            </tr>
        `;
        
        if (placeOrderBtn) {
            placeOrderBtn.style.display = 'none';
        }
    }
    
    // Show error message
    function showError(message) {
        console.error('🛒 [CHECKOUT] Error:', message);
        
        orderDetailsBody.innerHTML = `
            <tr>
                <td colspan="2" style="text-align: center; padding: 20px;">
                    <p style="color: #dc3545; font-size: 16px;">${message}</p>
                    <button onclick="location.reload()" class="btn btn-primary" style="margin-top: 10px;">Retry</button>
                </td>
            </tr>
        `;
        
        if (placeOrderBtn) {
            placeOrderBtn.style.display = 'none';
        }
    }
    
    // Handle place order button click
    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            console.log('🛒 [CHECKOUT] Place order button clicked');
            
            // Get form data
            const name = document.getElementById('customerName').value;
            const email = document.getElementById('customerEmail').value;
            const address = document.getElementById('customerAddress').value;
            const phone = document.getElementById('customerPhone').value;
            const message = document.getElementById('billMessage').value;
            
            // Validate required fields
            if (!name || !email || !address || !phone) {
                alert('Please fill in all required fields (Name, Email, Address, Phone)');
                return;
            }
            
            // Get cart data
            const currentCartData = window.cartData;
            if (!currentCartData || !currentCartData.items || currentCartData.items.length === 0) {
                alert('Your cart is empty!');
                return;
            }
            
            // Build WhatsApp message
            const whatsappMessage = buildWhatsAppMessage(name, email, address, phone, message, currentCartData);
            
            // Redirect to WhatsApp
            // Format: Country code (92) + number without leading 0
            const whatsappNumber = '923009845333';
            const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage)}`;
            
            console.log('🛒 [CHECKOUT] WhatsApp URL:', whatsappUrl);
            console.log('🛒 [CHECKOUT] Redirecting to WhatsApp...');
            
            // Try to open WhatsApp
            try {
                window.location.href = whatsappUrl;
            } catch (error) {
                console.error('🛒 [CHECKOUT] Error redirecting:', error);
                alert('Failed to open WhatsApp. Please try again.');
            }
        });
    }
    
    // Build WhatsApp message
    function buildWhatsAppMessage(name, email, address, phone, message, cartData) {
        let messageText = ` *New Order Request*\n\n`;
        messageText += `*Customer Information:*\n`;
        messageText += `Name: ${name}\n`;
        messageText += `Email: ${email}\n`;
        messageText += `Address: ${address}\n`;
        messageText += `Phone: ${phone}\n\n`;
        
        messageText += `*Order Details:*\n`;
        cartData.items.forEach((item, index) => {
            messageText += `${index + 1}. ${item.product.name}\n`;
            messageText += `   Quantity: ${item.quantity} x Rs ${item.product.current_price.toFixed(2)}\n`;
            messageText += `   Total: Rs ${item.total_price.toFixed(2)}\n\n`;
        });
        
        messageText += `*Summary:*\n`;
        messageText += `Subtotal: Rs ${cartData.total_price.toFixed(2)}\n`;
        messageText += `Shipping: Rs 50.00\n`;
        messageText += `*Grand Total: Rs ${(cartData.total_price + 50).toFixed(2)}*\n\n`;
        
        if (message && message.trim()) {
                messageText += `*Additional Message:*\n${message}\n`;
        }
        
        messageText += `\n*Order Date: ${new Date().toLocaleString()}`;
        
        return messageText;
    }
    
    // Initialize checkout on page load
    async function init() {
        console.log('🛒 [CHECKOUT] Initializing...');
        
        const cartData = await fetchCartData();
        if (cartData) {
            displayCartItems(cartData);
        }
        
        console.log('🛒 [CHECKOUT] Checkout initialized');
    }
    
    // Start the application
    init();
});
