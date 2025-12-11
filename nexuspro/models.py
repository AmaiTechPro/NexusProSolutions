from django.db import models
from django.conf import settings


# Create your models here.

class Register(models.Model):
    # The line that caused the error should be fixed like this:
    user = models.OneToOneField(
         settings.AUTH_USER_MODEL,  # <--- This is the 'to' argument
          on_delete=models.CASCADE   # <--- This is the 'on_delete' argument
)
    phonenumber= models.CharField
    account_status =models.CharField()
    is_tutor_candidate =models.BooleanField()
    current_location =models.CharField()
    career_focus =models.TextField()
    dob =models.DateField()
    profile_picture =models.ImageField()
    email_verification =models.BooleanField()
    registration_date = models.DateTimeField()



# nexuspro/models.py (or users/models.py, if you have a separate users app)

from django.db import models
from django.contrib.auth.models import User # Import the built-in user model

# Choices for the service_interest field
SERVICE_INTEREST_CHOICES = [
    ('networking', 'Networking & Labs (CCNA/CCNP)'),
    ('security', 'Cyber Security'),
    ('career', 'Career/CV Advisory'),
    ('business', 'Business Registration'),
    ('software', 'Software Development'),
]

class Profile(models.Model):
    # CRITICAL: Links the Profile model directly to the built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    
    # Custom Fields from edit_profile.html
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    service_interest = models.CharField(
        max_length=30, 
        choices=SERVICE_INTEREST_CHOICES, 
        default='networking'
    )
    
    # Optional field for a profile picture
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Note: You MUST use a signal (in signals.py) to automatically create a Profile 
# object whenever a new User object is created during registration.



# nexuspro/models.py

BOOKING_STATUS_CHOICES = [
    ('Pending', 'Pending Review'),
    ('Confirmed', 'Confirmed & Scheduled'),
    ('Completed', 'Service Completed'),
    ('Cancelled', 'Cancelled'),
]

SERVICE_TYPE_CHOICES = [
    ('ccna', 'CCNA/Network Tutoring'),
    ('ccnp', 'CCNP Advanced Training'),
    ('cyber', 'Cyber Security'),
    ('onsite', 'On-Site Technician'),
    ('remote', 'Remote IT Support'),
    ('cv_career', 'CV & Career Optimization'),
    ('biz_reg', 'Business Registration'),
    ('web_dev', 'Software Development'),
]

class Booking(models.Model):
    # Links the booking to the User who made it (Foreign Key)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    # Fields from book_consultation.html form
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    details = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Required for On-Site services.")

    # Status & Scheduling
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)
    session_date = models.DateTimeField(blank=True, null=True, help_text="Date and time when the session is scheduled.")

    def __str__(self):
        return f'Booking #{self.id} - {self.service_type}'
    
    class Meta:
        ordering = ['-request_date']




# nexuspro/models.py

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    service_provided = models.CharField(max_length=100, help_text="e.g., CCNP Training, CV Optimization")
    quote = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_approved = models.BooleanField(default=False) # Requires Admin approval before showing
    
    # Optional: If you want to link the testimonial to the user who wrote it
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'"{self.quote[:30]}..." by {self.client_name}'





























































