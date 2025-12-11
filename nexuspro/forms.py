     

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Booking, SERVICE_INTEREST_CHOICES # Import your models and choices

# ----------------------------------------------------------------------
# 1. Custom Registration Form (Handles User + Profile Creation)
# ----------------------------------------------------------------------

class UserAndProfileCreationForm(UserCreationForm):
    # Add User Model fields (First Name, Last Name)
    first_name = forms.CharField(max_length=150, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required.')
    email = forms.EmailField(required=True, help_text='Required. Must be a valid email address.')

    # Add Profile Model fields
    phone_number = forms.CharField(max_length=20, required=False, help_text='Your WhatsApp/mobile number.')
    service_interest = forms.ChoiceField(
        choices=SERVICE_INTEREST_CHOICES, 
        required=False,
        label='Primary Area of Interest'
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number', 'service_interest',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    # Custom save method to handle both User and Profile creation
    def save(self, commit=True):
        # 1. Save the User object first
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"] # Ensure email is saved to the User model
        
        if commit:
            user.save()
            
            # 2. Create the linked Profile object
            profile = Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get("phone_number"),
                service_interest=self.cleaned_data.get("service_interest"),
            )
            profile.save()
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





