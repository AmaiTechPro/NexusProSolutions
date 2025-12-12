from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import (
    UserAndProfileCreationForm, 
    UserEditForm, 
    ProfileEditForm, 
    BookingForm
)
from .models import Appointment, Booking, Profile, Testimonial # Ensure Testimonial is imported


# ======================================================================
# A. Static Page Views (Simple Renders - Only one function per template)
# ======================================================================

def index(request):
    """Home Page - Now passes dynamically approved testimonials."""
    
    # Fetch only testimonials that have been approved by the Admin
    approved_testimonials = Testimonial.objects.filter(is_approved=True).order_by('-rating', '?')[:6]
    
    context = {
        'testimonials': approved_testimonials
    }
    return render(request, 'index.html', context)

def base(request):
    return render(request, 'base.html')

def career(request):
    return render(request, 'career.html')

def registration(request):
    return render(request, 'registration.html')

def schedule(request):
    return render(request, 'schedule.html')


def bookings(request):
    return render(request, 'bookings.html')


def profile(request):
    return render(request, 'profile.html')


def it(request):
    return render(request, 'it.html')

# REMOVED: def editprofile(request): placeholder function to avoid conflict

def about(request):
    return render(request, 'about.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def testimonials(request):
    return render(request, 'testimonials.html')

def pricing(request):
    return render(request, 'pricing.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')









# Service/General Pages
def ccnp(request):
    return render(request, 'ccnp.html')

def network(request):
    return render(request, 'network.html')

def security(request):
    return render(request, 'security.html')

def technician(request):
    return render(request, 'technician.html')

def web(request):
    return render(request, 'web.html')

# Password Reset Placeholder Templates
def passwordform(request):
    return render(request, 'password_reset_form.html')

def passworddone(request):
    return render(request, 'password_reset_done.html')

def passwordconfirm(request):
    return render(request, 'password_reset_confirm.html')

def passwordcomplete(request):
    return render(request, 'password_reset_complete.html')

# ======================================================================
# B. Authentication & Registration Views (Functional)
# ======================================================================

def register_view(request):
    """Handles new user registration and Profile creation."""
    if request.method == 'POST':
        form = UserAndProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login') 
    else:
        form = UserAndProfileCreationForm()
        
    context = {'form': form}
    return render(request, 'register.html', context) 

# ======================================================================
# C. Account Management Views (Functional)
# ======================================================================

@login_required
def profile_view(request):
    """Displays the user dashboard and their current bookings."""
    
    bookings = Booking.objects.filter(user=request.user).order_by('-request_date')

    context = {
        'bookings': bookings,
        'user_profile': request.user.profile 
    }
    return render(request, 'profile.html', context) 

# **CONSOLIDATED AND CORRECTED edit_profile_view**
@login_required
@transaction.atomic
def edit_profile_view(request):
    """Handles editing of User and Profile details."""
    
    # Check if the user has a profile (crucial check, though signals should handle it)
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, "Your profile data is missing. Please contact support.")
        return redirect('profile')

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') 
    else:
        # CRITICAL: These lines fetch the existing data from the database
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=user_profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    # This renders the edit_profile.html template with the forms in the context
    return render(request, 'edit_profile.html', context)


# ======================================================================
# D. Booking View (Functional)
# ======================================================================

@login_required
def book_consultation_view(request):
    """Handles the form submission for a new booking."""
    
    initial_data = {}
    if 'service' in request.GET:
        initial_data['service_type'] = request.GET['service']
        
    if request.method == 'POST':
        form = BookingForm(request.POST) 
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user 
            booking.save()
            
            messages.success(request, 'Your booking request has been submitted successfully!')
            return redirect('bookings') 
    else:
        form = BookingForm(initial=initial_data)
        
    context = {'form': form}
    return render(request, 'bookings.html', context)





 



def contact(request):
    if request.method == 'POST':
        # 1. Capture data from the manual inputs
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        service = request.POST.get('service')
        message = request.POST.get('message')
        
        # 2. Validate and Save to your Appointment Model
        if fullname and email and service and message:
            Appointment.objects.create(
                fullname=fullname,
                email=email,
                service=service, # Ensure 'service' matches your model field
                message=message
            )
            messages.success(request, 'Your request has been successfully submitted! We will contact you shortly.')
            return redirect('contact') # Redirect to the same page
        else:
            messages.error(request, 'Please fill out all required fields.')
    
    # Render the template (for GET requests or failed POST requests)
    return render(request, 'contact.html')













# nexuspro/views.py (Add this new view function)

from .forms import (
    # ... other forms ...
    TestimonialForm # <-- ADD THIS IMPORT
)
# ... other imports ...

# ======================================================================
# E. Testimonial Submission View (Functional)
# ======================================================================

@login_required
def submit_testimonial_view(request):
    """Allows logged-in users to submit a new testimonial."""
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST) 
        if form.is_valid():
            testimonial = form.save(commit=False)
            
            # CRITICAL SECURITY STEP: Associate the review with the logged-in user
            testimonial.user = request.user 
            
            # Set client_name automatically for simplicity and consistency
            if not testimonial.client_name:
                 testimonial.client_name = f"{request.user.first_name} {request.user.last_name}"
                 
            testimonial.save()
            
            messages.success(request, 'Thank you! Your testimonial has been submitted for review.')
            return redirect('submit_testimonial') # Redirect to dashboard after successful submission
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill client name for convenience
        initial_data = {
            'client_name': f"{request.user.first_name} {request.user.last_name}"
        }
        form = TestimonialForm(initial=initial_data)
        
    context = {'form': form}
    return render(request, 'submit_testimonial.html', context)