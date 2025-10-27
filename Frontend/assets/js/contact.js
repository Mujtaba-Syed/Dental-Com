// Contact page functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('📞 [CONTACT] Initializing contact page...');
    
    // Get the form element
    const contactForm = document.getElementById('contactForm');
    
    // Handle form submission
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('📞 [CONTACT] Form submitted');
            
            // Get form data
            const name = document.getElementById('contactName').value.trim();
            const email = document.getElementById('contactEmail').value.trim();
            const phone = document.getElementById('contactPhone').value.trim();
            const subject = document.getElementById('contactSubject').value.trim();
            const message = document.getElementById('contactMessage').value.trim();
            
            // Validate required fields
            if (!name || !email || !phone || !subject || !message) {
                alert('Please fill in all fields');
                return;
            }
            
            // Build WhatsApp message
            const whatsappMessage = buildWhatsAppMessage(name, email, phone, subject, message);
            
            // Redirect to WhatsApp
            const whatsappNumber = '923009845333';
            const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage)}`;
            
            console.log('📞 [CONTACT] WhatsApp URL:', whatsappUrl);
            console.log('📞 [CONTACT] Redirecting to WhatsApp...');
            
            // Redirect to WhatsApp
            try {
                window.location.href = whatsappUrl;
            } catch (error) {
                console.error('📞 [CONTACT] Error redirecting:', error);
                alert('Failed to open WhatsApp. Please try again.');
            }
        });
    }
    
    // Build WhatsApp message
    function buildWhatsAppMessage(name, email, phone, subject, message) {
        let messageText = `*New Contact Form Submission*\n\n`;
        messageText += `*Customer Information:*\n`;
        messageText += `Name: ${name}\n`;
        messageText += `Email: ${email}\n`;
        messageText += `Phone: ${phone}\n\n`;
        messageText += `*Subject:*\n${subject}\n\n`;
        messageText += `*Message:*\n${message}\n\n`;
        messageText += `*Submission Date:* ${new Date().toLocaleString()}`;
        
        return messageText;
    }
    
    console.log('📞 [CONTACT] Contact page initialized');
});
