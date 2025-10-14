// Shop page functionality
document.addEventListener('DOMContentLoaded', function() {
    const productContainer = document.getElementById('product-container');
    const filterButtons = document.querySelectorAll('.product-filters li');
    
    // Debug: Check if products are loaded
    // console.log('Shop.js loaded. Products:', products);
    // console.log('Product container:', productContainer);
    
    // Render products function
    function renderProducts(productsToRender = products) {
        // console.log('Rendering products:', productsToRender);
        if (!productContainer) {
            // console.error('Product container not found!');
            return;
        }
        
        productContainer.innerHTML = '';
        
        if (!productsToRender || productsToRender.length === 0) {
            // console.log('No products to render');
            productContainer.innerHTML = '<div class="col-12 text-center"><p>No products found.</p></div>';
            return;
        }
        
        productsToRender.forEach((product, index) => {
            // console.log(`Creating product ${index + 1}:`, product);
            const productElement = createProductElement(product);
            productContainer.appendChild(productElement);
        });
        
        // Force the container to show content
        productContainer.style.height = 'auto';
        productContainer.style.minHeight = '200px';
        
        // console.log('Product container after adding products:', productContainer);
        // console.log('Number of child elements:', productContainer.children.length);
        
        // Initialize isotope after rendering (commented out for debugging)
        // if (typeof $ !== 'undefined' && $.fn.isotope) {
        //     $('.product-lists').isotope({
        //         itemSelector: '.single-product-item',
        //         layoutMode: 'fitRows'
        //     });
        // }
    }
    
    // Create product element
    function createProductElement(product) {
        // console.log('Creating product element for:', product.name, 'Images:', product.images);
        const col = document.createElement('div');
        col.className = `col-lg-4 col-md-6 text-center ${product.category}`;
        
        // Get primary image - handle both primary_image and images array
        let imageUrl = '/static/img/products/product-img-1.jpg';
        let imageAlt = product.name;
        
        if (product.primary_image && product.primary_image.image) {
            imageUrl = product.primary_image.image;
            imageAlt = product.primary_image.alt_text || product.name;
        } else if (product.images && Array.isArray(product.images) && product.images.length > 0) {
            const primaryImage = product.images.find(img => img.is_primary) || product.images[0];
            if (primaryImage) {
                imageUrl = primaryImage.image;
                imageAlt = primaryImage.alt_text || product.name;
            }
        }
        
        // Format price
        const price = parseFloat(product.price);
        const salePrice = product.sale_price ? parseFloat(product.sale_price) : null;
        const displayPrice = salePrice || price;
        const originalPrice = salePrice ? price : null;
        
        col.innerHTML = `
            <div class="single-product-item">
                <div class="product-image">
                    <a href="/product/${product.id}/">
                        <img src="${imageUrl}" alt="${imageAlt}">
                    </a>
                    ${product.on_sale ? '<span class="sale-badge">Sale</span>' : ''}
                </div>
                <h3>${product.name}</h3>
                <p class="product-price">
                    ${originalPrice ? `<span class="original-price">Rs ${originalPrice.toFixed(2)}</span>` : ''}
                    <span class="current-price">Rs ${displayPrice.toFixed(2)}</span>
                </p>
                <a href="/cart/" class="cart-btn" data-product-id="${product.id}">
                    <i class="fas fa-shopping-cart"></i> Add to Cart
                </a>
            </div>
        `;
        
        // console.log('Created product element HTML:', col.outerHTML);
        return col;
    }
    
    // Filter functionality
    function setupFilters() {
        let filteredProducts = products;
        
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // console.log('Filter clicked:', this.textContent, 'data-filter:', this.getAttribute('data-filter'));
                
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                
                if (filter === '*') {
                    filteredProducts = products;
                    // console.log('Showing all products:', filteredProducts.length);
                } else {
                    const category = filter.replace('.', '');
                    filteredProducts = products.filter(product => product.category === category);
                    // console.log(`Filtering by category '${category}':`, filteredProducts.length, 'products found');
                }
                
                // Update pagination for filtered results
                updatePaginationForFilteredProducts(filteredProducts);
                // Render first page of filtered results
                const itemsPerPage = 6;
                const firstPageProducts = filteredProducts.slice(0, itemsPerPage);
                renderProducts(firstPageProducts);
            });
        });
        
        // Function to update pagination for filtered products
        function updatePaginationForFilteredProducts(filteredProducts) {
            const paginationContainer = document.querySelector('.pagination-wrap ul');
            if (!paginationContainer) return;
            
            const itemsPerPage = 6;
            const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);
            let currentPage = 1;
            
            // Clear existing pagination
            paginationContainer.innerHTML = '';
            
            if (totalPages <= 1) {
                paginationContainer.innerHTML = '';
                return;
            }
            
            // Create pagination buttons
            function createPaginationButtons() {
                paginationContainer.innerHTML = '';
                
                // Previous button
                const prevBtn = document.createElement('li');
                prevBtn.innerHTML = '<a href="#" class="prev-btn">Prev</a>';
                prevBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (currentPage > 1) {
                        currentPage--;
                        updatePagination();
                        const startIndex = (currentPage - 1) * itemsPerPage;
                        const endIndex = startIndex + itemsPerPage;
                        renderProducts(filteredProducts.slice(startIndex, endIndex));
                    }
                });
                paginationContainer.appendChild(prevBtn);
                
                // Page numbers
                for (let i = 1; i <= totalPages; i++) {
                    const pageBtn = document.createElement('li');
                    pageBtn.innerHTML = `<a href="#" class="page-btn" data-page="${i}">${i}</a>`;
                    if (i === currentPage) {
                        pageBtn.querySelector('a').classList.add('active');
                    }
                    pageBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        currentPage = i;
                        updatePagination();
                        const startIndex = (currentPage - 1) * itemsPerPage;
                        const endIndex = startIndex + itemsPerPage;
                        renderProducts(filteredProducts.slice(startIndex, endIndex));
                    });
                    paginationContainer.appendChild(pageBtn);
                }
                
                // Next button
                const nextBtn = document.createElement('li');
                nextBtn.innerHTML = '<a href="#" class="next-btn">Next</a>';
                nextBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (currentPage < totalPages) {
                        currentPage++;
                        updatePagination();
                        const startIndex = (currentPage - 1) * itemsPerPage;
                        const endIndex = startIndex + itemsPerPage;
                        renderProducts(filteredProducts.slice(startIndex, endIndex));
                    }
                });
                paginationContainer.appendChild(nextBtn);
            }
            
            function updatePagination() {
                const pageBtns = paginationContainer.querySelectorAll('.page-btn');
                pageBtns.forEach(btn => {
                    btn.classList.remove('active');
                    if (parseInt(btn.dataset.page) === currentPage) {
                        btn.classList.add('active');
                    }
                });
                
                // Update prev/next button states
                const prevBtn = paginationContainer.querySelector('.prev-btn');
                const nextBtn = paginationContainer.querySelector('.next-btn');
                
                if (prevBtn) {
                    prevBtn.style.opacity = currentPage === 1 ? '0.5' : '1';
                    prevBtn.style.pointerEvents = currentPage === 1 ? 'none' : 'auto';
                }
                
                if (nextBtn) {
                    nextBtn.style.opacity = currentPage === totalPages ? '0.5' : '1';
                    nextBtn.style.pointerEvents = currentPage === totalPages ? 'none' : 'auto';
                }
            }
            
            
            // Initialize pagination
            createPaginationButtons();
            updatePagination();
        }
    }
    
    // Add to cart functionality
    function setupAddToCart() {
        document.addEventListener('click', function(e) {
            if (e.target.closest('.cart-btn')) {
                e.preventDefault();
                const productId = e.target.closest('.cart-btn').getAttribute('data-product-id');
                addToCart(productId);
            }
        });
    }
    
    // Add to cart function
    function addToCart(productId) {
        // Get existing cart from localStorage
        let cart = JSON.parse(localStorage.getItem('cart') || '[]');
        
        // Check if product already in cart
        const existingItem = cart.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            const product = products.find(p => p.id == productId);
            if (product) {
                cart.push({
                    productId: productId,
                    name: product.name,
                    price: product.sale_price || product.price,
                    image: (product.primary_image && product.primary_image.image) ? product.primary_image.image : 
                           ((product.images && product.images.length > 0) ? product.images[0].image : '/static/img/products/product-img-1.jpg'),
                    quantity: 1
                });
            }
        }
        
        // Save cart to localStorage
        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Show success message
        showNotification('Product added to cart!', 'success');
        
        // Update cart count if element exists
        updateCartCount();
    }
    
    // Show notification
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#4CAF50' : '#2196F3'};
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            z-index: 9999;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    // Update cart count
    function updateCartCount() {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        
        // Update cart count in navbar if it exists
        const cartCountElement = document.querySelector('.cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = totalItems;
        }
    }
    
    // Pagination functionality
    function setupPagination() {
        const paginationContainer = document.querySelector('.pagination-wrap ul');
        if (!paginationContainer) return;
        
        // Clear existing pagination
        paginationContainer.innerHTML = '';
        
        const itemsPerPage = 6;
        const totalPages = Math.ceil(products.length / itemsPerPage);
        let currentPage = 1;
        
        // Create pagination buttons
        function createPaginationButtons() {
            paginationContainer.innerHTML = '';
            
            // Previous button
            const prevBtn = document.createElement('li');
            prevBtn.innerHTML = '<a href="#" class="prev-btn">Prev</a>';
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (currentPage > 1) {
                    currentPage--;
                    updatePagination();
                    renderProducts(getCurrentPageProducts());
                }
            });
            paginationContainer.appendChild(prevBtn);
            
            // Page numbers
            for (let i = 1; i <= totalPages; i++) {
                const pageBtn = document.createElement('li');
                pageBtn.innerHTML = `<a href="#" class="page-btn" data-page="${i}">${i}</a>`;
                if (i === currentPage) {
                    pageBtn.querySelector('a').classList.add('active');
                }
                pageBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    currentPage = i;
                    updatePagination();
                    renderProducts(getCurrentPageProducts());
                });
                paginationContainer.appendChild(pageBtn);
            }
            
            // Next button
            const nextBtn = document.createElement('li');
            nextBtn.innerHTML = '<a href="#" class="next-btn">Next</a>';
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (currentPage < totalPages) {
                    currentPage++;
                    updatePagination();
                    renderProducts(getCurrentPageProducts());
                }
            });
            paginationContainer.appendChild(nextBtn);
        }
        
        function updatePagination() {
            const pageBtns = paginationContainer.querySelectorAll('.page-btn');
            pageBtns.forEach(btn => {
                btn.classList.remove('active');
                if (parseInt(btn.dataset.page) === currentPage) {
                    btn.classList.add('active');
                }
            });
            
            // Update prev/next button states
            const prevBtn = paginationContainer.querySelector('.prev-btn');
            const nextBtn = paginationContainer.querySelector('.next-btn');
            
            if (prevBtn) {
                prevBtn.style.opacity = currentPage === 1 ? '0.5' : '1';
                prevBtn.style.pointerEvents = currentPage === 1 ? 'none' : 'auto';
            }
            
            if (nextBtn) {
                nextBtn.style.opacity = currentPage === totalPages ? '0.5' : '1';
                nextBtn.style.pointerEvents = currentPage === totalPages ? 'none' : 'auto';
            }
        }
        
        function getCurrentPageProducts() {
            const startIndex = (currentPage - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;
            return products.slice(startIndex, endIndex);
        }
        
        // Initialize pagination
        createPaginationButtons();
        updatePagination();
        
        // Store pagination functions globally for filter updates
        window.updatePagination = updatePagination;
        window.getCurrentPageProducts = getCurrentPageProducts;
        window.currentPage = () => currentPage;
    }
    
    // Initialize everything
    function init() {
        // console.log('Initializing shop...');
        
        // Debug: Show available categories
        const categories = [...new Set(products.map(p => p.category))];
        // console.log('Available product categories:', categories);
        
        setupPagination();
        // Render first page of products
        const itemsPerPage = 6;
        const firstPageProducts = products.slice(0, itemsPerPage);
        renderProducts(firstPageProducts);
        setupFilters();
        setupAddToCart();
        updateCartCount();
    }
    
    // Start the application
    init();
});