     

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SERVICE_TYPE_CHOICES, Profile, Booking, SERVICE_INTEREST_CHOICES, Testimonial # Import your models and choices
from django.db import transaction
# ----------------------------------------------------------------------
# 1. Custom Registration Form (Handles User + Profile Creation)
# 




# CRITICAL FIX: Base the form on the User model
class UserAndProfileCreationForm(forms.ModelForm):
    # This form explicitly includes fields from User and Profile models.

    # 1. Define Fields explicitly (passwords are standard, non-model fields)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")

    # 2. Define the Meta class based on the PRIMARY model (User)
    class Meta:
        model = User # <--- CRITICAL: MUST SPECIFY THE MODEL
        fields = ('username', 'first_name', 'last_name', 'email')
        
    # 3. Add fields from the secondary model (Profile) outside the Meta class
    phone_number = forms.CharField(max_length=20, required=False, label="Phone Number")
    service_interest = forms.ChoiceField(
        # Assuming you defined SERVICE_TYPE_CHOICES somewhere in your forms.py or models.py
        choices=SERVICE_TYPE_CHOICES, # <--- ENSURE THIS IS DEFINED AND IMPORTED
        required=False,
        label="Primary Service Interest"
    )

    # 4. Clean method for password validation (Security)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError(
                "Passwords must match."
            )
        return cleaned_data

    # 5. Save method (The one we fixed earlier to prevent double-creation)
    @transaction.atomic
    def save(self, commit=True):
        # 1. Save the User object first
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data["password"])
        user.save()

        # 2. Safely create or update the Profile
        profile_data = {
            'phone_number': self.cleaned_data.get('phone_number'),
            'service_interest': self.cleaned_data.get('service_interest'),
            # Ensure other Profile fields like bio, etc., are handled if present
        }
        
        # Use update_or_create to handle both new registration (create) and submission errors (update)
        Profile.objects.update_or_create(user=user, defaults=profile_data)

        return user





# ----------------------------------------------------------------------
# 2. Profile Editing Form (Handles Profile fields only)
# ----------------------------------------------------------------------

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'bio', 'service_interest']

# ----------------------------------------------------------------------
# 3. User Editing Form (Handles base User fields only)
# ----------------------------------------------------------------------

class UserEditForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# ----------------------------------------------------------------------
# 4. Booking Form (For the book_consultation page)
# ----------------------------------------------------------------------

class BookingForm(forms.ModelForm):
    # Add non-model fields here if needed (e.g., location input)
    
    class Meta:
        model = Booking
        # Note: We exclude 'user', 'status', 'request_date', 'session_date' as they are set in the view
        fields = ['service_type', 'details', 'location']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4}),
        }






# nexuspro/forms.py (Add this new form)


# ... (Keep your other imports: UserEditForm, ProfileEditForm, BookingForm, etc.)

# Testimonial Submission Form
class TestimonialForm(forms.ModelForm):
    # Ensure the Rating field uses RadioSelect for better rendering in the template
    rating = forms.IntegerField(
        widget=forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        label="Rating (1-5 Stars)"
    )

    class Meta:
        model = Testimonial
        # Exclude fields that must be set securely in the view
        fields = ['client_name', 'service_provided', 'quote', 'rating'] 
        widgets = {
            'quote': forms.Textarea(attrs={'rows': 4}),
        }
