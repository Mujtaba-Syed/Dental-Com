// Global utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function getBackgroundClass(index) {
    const bgClasses = ['news-bg-1', 'news-bg-2', 'news-bg-3', 'news-bg-4', 'news-bg-5', 'news-bg-6'];
    return bgClasses[index % bgClasses.length];
}

// Add CSS for consistent card heights
function addCardHeightStyles() {
    // Check if styles already exist
    if (document.getElementById('news-card-styles')) {
        return;
    }
    
    const style = document.createElement('style');
    style.id = 'news-card-styles';
    style.textContent = `
        .single-latest-news {
            min-height: 520px !important;
            display: flex !important;
            flex-direction: column !important;
            height: 520px !important;
        }
        .news-text-box {
            flex: 1 !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
        }
        .news-description {
            flex: 1 !important;
            display: flex !important;
            align-items: flex-start !important;
            min-height: 60px !important;
        }
        .latest-news-bg {
            height: 200px !important;
            background-size: cover !important;
            background-position: center !important;
        }
    `;
    document.head.appendChild(style);
    console.log('Card height styles applied');
}

// Get BASE_URL from Django template variable or use default
const BASE_URL = window.DJANGO_CONFIG?.BASE_URL || 'http://127.0.0.1:8000/api/';
// News dynamic rendering functionality using template-based approach
document.addEventListener('DOMContentLoaded', function() {
    console.log('News.js loaded and DOM ready');
    
    // Add CSS styles for consistent card heights
    addCardHeightStyles();
    
    const newsContainer = document.getElementById('news-container');
    const loadingSpinner = document.getElementById('loading-spinner');
    const paginationList = document.getElementById('pagination-list');
    
    console.log('Elements found:', {
        newsContainer: !!newsContainer,
        loadingSpinner: !!loadingSpinner,
        paginationList: !!paginationList
    });
    
    // API endpoint
    const API_URL = `${BASE_URL}blog/posts/`;
    
    // Function to populate news card from template
    function populateNewsCard(template, post, index) {
        // Get the template element
        const newsCard = template.cloneNode(true);
        newsCard.style.display = 'block'; // Make it visible
        
        // Ensure styles are applied
        addCardHeightStyles();
        
        // Update background class
        const newsImage = newsCard.querySelector('.news-image');
        newsImage.className = `latest-news-bg ${getBackgroundClass(index)} news-image`;
        
        // Set background image if available
        if (post.image) {
            newsImage.style.backgroundImage = `url('${post.image}')`;
        }
        
        // Update links
        const newsLink = newsCard.querySelector('.news-link');
        const titleLink = newsCard.querySelector('.news-title-link');
        const readMoreLink = newsCard.querySelector('.news-read-more');
        
        newsLink.href = `/news/${post.id}/`;
        titleLink.href = `/news/${post.id}/`;
        readMoreLink.href = `/news/${post.id}/`;
        
        // Update content
        titleLink.textContent = post.title;
        
        const authorName = post.author.first_name && post.author.last_name 
            ? `${post.author.first_name} ${post.author.last_name}`.trim()
            : post.author.username;
        newsCard.querySelector('.author-name').textContent = authorName;
        
        newsCard.querySelector('.news-date').textContent = formatDate(post.created_at);
        
        // Truncate description to keep card size consistent
        const description = post.description;
        const truncatedDescription = description.length > 120 ? description.substring(0, 120) + '...' : description;
        newsCard.querySelector('.news-description').textContent = truncatedDescription;
        
        return newsCard;
    }
    
    // Function to render pagination
    function renderPagination(data) {
        if (!paginationList) return;
        
        paginationList.innerHTML = '';
        
        // Previous button
        const prevLi = document.createElement('li');
        const prevLink = document.createElement('a');
        prevLink.href = '#';
        prevLink.textContent = 'Prev';
        if (data.previous) {
            prevLink.onclick = (e) => {
                e.preventDefault();
                loadNews(data.previous);
            };
        } else {
            prevLink.classList.add('disabled');
        }
        prevLi.appendChild(prevLink);
        paginationList.appendChild(prevLi);
        
        // Page numbers (simplified - you can enhance this)
        const totalPages = Math.ceil(data.count / 6);
        for (let i = 1; i <= totalPages; i++) {
            const pageLi = document.createElement('li');
            const pageLink = document.createElement('a');
            pageLink.href = '#';
            pageLink.textContent = i;
            pageLink.onclick = (e) => {
                e.preventDefault();
                loadNews(`${API_URL}?page=${i}`);
            };
            if (i === 1) pageLink.classList.add('active');
            pageLi.appendChild(pageLink);
            paginationList.appendChild(pageLi);
        }
        
        // Next button
        const nextLi = document.createElement('li');
        const nextLink = document.createElement('a');
        nextLink.href = '#';
        nextLink.textContent = 'Next';
        if (data.next) {
            nextLink.onclick = (e) => {
                e.preventDefault();
                loadNews(data.next);
            };
        } else {
            nextLink.classList.add('disabled');
        }
        nextLi.appendChild(nextLink);
        paginationList.appendChild(nextLi);
    }
    
    // Function to load news data
    async function loadNews(url = API_URL) {
        console.log('Loading news from:', url);
        try {
            if (loadingSpinner) {
                loadingSpinner.style.display = 'block';
            }
            
            const response = await fetch(url);
            console.log('API Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('API Data received:', data);
            
            if (newsContainer) {
                console.log('News container found, processing data...');
                
                // Clear existing content except template
                const template = newsContainer.querySelector('.news-template');
                console.log('Template found:', !!template);
                
                const existingCards = newsContainer.querySelectorAll('.col-lg-4.col-md-6:not(.news-template)');
                console.log('Existing cards to remove:', existingCards.length);
                existingCards.forEach(card => card.remove());
                
                if (data.results && data.results.length > 0) {
                    console.log('Processing', data.results.length, 'news articles');
                    data.results.forEach((post, index) => {
                        console.log('Creating card for post:', post.title);
                        const newsCard = populateNewsCard(template, post, index);
                        newsContainer.appendChild(newsCard);
                    });
                } else {
                    console.log('No news articles found');
                    const noNewsDiv = document.createElement('div');
                    noNewsDiv.className = 'col-12 text-center';
                    noNewsDiv.innerHTML = '<p>No news articles found.</p>';
                    newsContainer.appendChild(noNewsDiv);
                }
            } else {
                console.error('News container not found!');
            }
            
            renderPagination(data);
            
        } catch (error) {
            console.error('Error loading news:', error);
            if (newsContainer) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'col-12 text-center';
                errorDiv.innerHTML = '<p>Error loading news articles. Please try again later.</p>';
                newsContainer.appendChild(errorDiv);
            }
        } finally {
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }
        }
    }
    
    // Only load news if we're on the news page (not index page)
    if (newsContainer) {
        // Test API connectivity first
        console.log('Testing API connectivity...');
        fetch(API_URL)
            .then(response => {
                console.log('API Test Response:', response.status);
                if (response.ok) {
                    console.log('API is accessible');
                    loadNews();
                } else {
                    console.error('API returned error:', response.status);
                    // Show error message
                    if (newsContainer) {
                        newsContainer.innerHTML = '<div class="col-12 text-center"><p>API Error: ' + response.status + '</p></div>';
                    }
                }
            })
            .catch(error => {
                console.error('API Test Failed:', error);
                // Show error message
                if (newsContainer) {
                    newsContainer.innerHTML = '<div class="col-12 text-center"><p>Cannot connect to API. Please check if the backend server is running.</p></div>';
                }
            });
    }
});

// Single news page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the single news page (URL pattern: /news/{id}/)
    const pathMatch = window.location.pathname.match(/^\/news\/(\d+)\/$/);
    if (pathMatch) {
        console.log('Single news page detected');
        loadSingleNews();
    }
    
    // Check if we're on the index page and load latest news
    if (window.location.pathname === '/' || window.location.pathname === '/home/') {
        console.log('Index page detected, loading latest news');
        loadIndexNews();
    }
});

// Function to load single news article
async function loadSingleNews() {
    console.log('Loading single news article...');
    console.log('Current URL:', window.location.href);
    
    // Get the blog ID from URL path (pattern: /news/{id}/)
    const pathMatch = window.location.pathname.match(/^\/news\/(\d+)\/$/);
    const blogId = pathMatch ? pathMatch[1] : null;
    
    console.log('URL path:', window.location.pathname);
    console.log('Blog ID found:', blogId);
    
    if (!blogId) {
        console.error('No blog ID found in URL path');
        showError('No blog article specified. Please go back to the news page and click on an article.');
        return;
    }
    
    console.log('Loading blog with ID:', blogId);
    
    try {
        // Show loading state
        const loadingElement = document.getElementById('loading-spinner');
        if (loadingElement) {
            loadingElement.style.display = 'block';
        }
        
        // Fetch the specific blog post
        const response = await fetch(`${BASE_URL}blog/posts/${blogId}/`);
        console.log('Single news API Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const blogPost = await response.json();
        console.log('Single news data received:', blogPost);
        
        // Populate the single news page
        populateSingleNews(blogPost);
        
    } catch (error) {
        console.error('Error loading single news:', error);
        showError('Error loading blog article. Please try again later.');
    } finally {
        // Hide loading state
        const loadingElement = document.getElementById('loading-spinner');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
    }
}

// Function to populate single news page content
function populateSingleNews(blogPost) {
    console.log('Populating single news page...');
    
    // Update page title
    document.title = blogPost.title + ' | DentalCom';
    
    // Update meta description if available
    if (blogPost.meta_description) {
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) {
            metaDesc.setAttribute('content', blogPost.meta_description);
        }
    }
    
    // Format date
    const formattedDate = formatDate(blogPost.created_at);
    
    // Get author name
    const authorName = blogPost.author.first_name && blogPost.author.last_name 
        ? `${blogPost.author.first_name} ${blogPost.author.last_name}`.trim()
        : blogPost.author.username;
    
    // Update article content
    const articleSection = document.querySelector('.single-article-section');
    if (articleSection) {
        // Update background image
        const articleBg = articleSection.querySelector('.single-artcile-bg');
        if (articleBg && blogPost.image) {
            articleBg.style.backgroundImage = `url('${blogPost.image}')`;
        }
        
        // Update meta information
        const authorNameElement = articleSection.querySelector('.author-name');
        const newsDateElement = articleSection.querySelector('.news-date');
        
        if (authorNameElement) {
            authorNameElement.textContent = authorName;
        }
        if (newsDateElement) {
            newsDateElement.textContent = formattedDate;
        }
        
        // Update title
        const titleElement = articleSection.querySelector('.article-title');
        if (titleElement) {
            titleElement.textContent = blogPost.title;
        }
        
        // Update content
        const contentElement = articleSection.querySelector('.article-content');
        if (contentElement) {
            // Clear existing content
            contentElement.innerHTML = '';
            
            // Split content by double line breaks and create paragraphs
            const contentParts = blogPost.content.split('\r\n\r\n');
            contentParts.forEach(part => {
                if (part.trim()) {
                    const p = document.createElement('p');
                    p.textContent = part.trim();
                    contentElement.appendChild(p);
                }
            });
        }
    }
    
    // Update sidebar with dynamic data
    updateSidebarTags(blogPost.keywords_list || []);
    updateSidebarRecentPosts();
    
    console.log('Single news page populated successfully');
}


// Function to show error message
function showError(message) {
    const articleSection = document.querySelector('.single-article-section');
    if (articleSection) {
        articleSection.innerHTML = `
            <div class="text-center">
                <h2>Error</h2>
                <p>${message}</p>
                <a href="news.html" class="btn btn-primary">Back to News</a>
            </div>
        `;
    }
}

// Function to update sidebar recent posts
async function updateSidebarRecentPosts() {
    console.log('Loading recent posts for sidebar...');
    
    try {
        // Fetch recent posts from API
        const response = await fetch(`${BASE_URL}blog/posts/?limit=5`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Recent posts data:', data);
        
        // Update recent posts in sidebar
        const recentPostsList = document.querySelector('.recent-posts ul');
        if (recentPostsList && data.results) {
            recentPostsList.innerHTML = '';
            
            data.results.forEach(post => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = `/news/${post.id}/`;
                a.textContent = post.title;
                li.appendChild(a);
                recentPostsList.appendChild(li);
            });
        }
        
    } catch (error) {
        console.error('Error loading recent posts:', error);
    }
}

// Function to update sidebar tags with keywords from API
function updateSidebarTags(keywords) {
    console.log('Updating sidebar tags with keywords:', keywords);
    
    const tagsList = document.querySelector('.tag-section ul');
    if (tagsList) {
        tagsList.innerHTML = '';
        
        if (keywords && keywords.length > 0) {
            keywords.forEach(keyword => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = '#'; // You can enhance this to filter by tag later
                a.textContent = keyword;
                li.appendChild(a);
                tagsList.appendChild(li);
            });
        } else {
            // Show default message if no keywords
            const li = document.createElement('li');
            li.textContent = 'No tags available';
            tagsList.appendChild(li);
        }
    }
}

// Function to load latest 3 news articles for index page
async function loadIndexNews() {
    console.log('Loading latest news for index page...');
    
    const newsContainer = document.getElementById('index-news-container');
    const loadingSpinner = document.getElementById('news-loading-spinner');
    
    if (!newsContainer) {
        console.error('Index news container not found');
        return;
    }
    
    try {
        // Show loading state
        if (loadingSpinner) {
            loadingSpinner.style.display = 'block';
        }
        
        // Fetch latest 3 news articles
        const response = await fetch(`${BASE_URL}blog/posts/?limit=3`);
        console.log('Index news API Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Index news data received:', data);
        
        // Clear existing content except template
        const template = newsContainer.querySelector('.news-template');
        const existingCards = newsContainer.querySelectorAll('.col-lg-4.col-md-6:not(.news-template)');
        existingCards.forEach(card => card.remove());
        
        if (data.results && data.results.length > 0) {
            console.log('Processing', data.results.length, 'news articles for index');
            data.results.forEach((post, index) => {
                console.log('Creating index card for post:', post.title);
                const newsCard = populateIndexNewsCard(template, post, index);
                newsContainer.appendChild(newsCard);
            });
        } else {
            console.log('No news articles found for index');
            const noNewsDiv = document.createElement('div');
            noNewsDiv.className = 'col-12 text-center';
            noNewsDiv.innerHTML = '<p>No news articles found.</p>';
            newsContainer.appendChild(noNewsDiv);
        }
        
    } catch (error) {
        console.error('Error loading index news:', error);
        if (newsContainer) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'col-12 text-center';
            errorDiv.innerHTML = '<p>Error loading news articles. Please try again later.</p>';
            newsContainer.appendChild(errorDiv);
        }
    } finally {
        // Hide loading state
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
    }
}

// Function to populate index news card from template
function populateIndexNewsCard(template, post, index) {
    // Get the template element
    const newsCard = template.cloneNode(true);
    newsCard.style.display = 'block'; // Make it visible
    
    // Ensure styles are applied
    addCardHeightStyles();
    
    // Update background class
    const newsImage = newsCard.querySelector('.news-image');
    newsImage.className = `latest-news-bg ${getBackgroundClass(index)} news-image`;
    
    // Set background image if available
    if (post.image) {
        newsImage.style.backgroundImage = `url('${post.image}')`;
    }
    
    // Update links
    const newsLink = newsCard.querySelector('.news-link');
    const titleLink = newsCard.querySelector('.news-title-link');
    const readMoreLink = newsCard.querySelector('.news-read-more');
    
    newsLink.href = `/news/${post.id}/`;
    titleLink.href = `/news/${post.id}/`;
    readMoreLink.href = `/news/${post.id}/`;
    
    // Update content
    titleLink.textContent = post.title;
    
    const authorName = post.author.first_name && post.author.last_name 
        ? `${post.author.first_name} ${post.author.last_name}`.trim()
        : post.author.username;
    newsCard.querySelector('.author-name').textContent = authorName;
    
    newsCard.querySelector('.news-date').textContent = formatDate(post.created_at);
    
    // Truncate description to keep card size consistent
    const description = post.description;
    const truncatedDescription = description.length > 100 ? description.substring(0, 100) + '...' : description;
    newsCard.querySelector('.news-description').textContent = truncatedDescription;
    
    return newsCard;
} 