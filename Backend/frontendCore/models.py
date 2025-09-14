from django.db import models
from django.utils import timezone

# Create your models here.

class Appointment(models.Model):
    """Model for storing appointment bookings"""
    
    SERVICE_CHOICES = [
        ('general_checkup', 'General Checkup'),
        ('cleaning', 'Teeth Cleaning'),
        ('filling', 'Dental Filling'),
        ('extraction', 'Tooth Extraction'),
        ('crown', 'Dental Crown'),
        ('root_canal', 'Root Canal Treatment'),
        ('orthodontics', 'Orthodontics Consultation'),
        ('cosmetic', 'Cosmetic Dentistry'),
        ('emergency', 'Emergency Treatment'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Patient information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Appointment details
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField(blank=True, null=True)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.appointment_date} {self.appointment_time}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def formatted_phone(self):
        """Format phone number for display"""
        if len(self.phone) == 10:
            return f"({self.phone[:3]}) {self.phone[3:6]}-{self.phone[6:]}"
        return self.phone
