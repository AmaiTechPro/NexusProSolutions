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
from .models import Booking, Profile 


# ======================================================================
# A. Static Page Views (Simple Renders - Only one function per template)
# ======================================================================

def index(request):
    return render(request, 'index.html')

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

def editprofile(request):
    return render(request, 'edit_profile.html')

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

def contact(request):
    return render(request, 'contact.html')

# Service/General Pages (Kept the descriptive names where functional logic is elsewhere)
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

# The following views are placeholders for templates, but we use Django Auth views for the logic:
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
#    - Note: login and logout views are now handled entirely in urls.py
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


@login_required
@transaction.atomic
def edit_profile_view(request):
    """Handles editing of User and Profile details."""
    
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') 
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
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
            
            messages.success(request, 'Your booking request has been submitted!')
            return redirect('profile') 
    else:
        form = BookingForm(initial=initial_data)
        
    context = {'form': form}
    # IMPORTANT: Ensure this maps to your booking form template
    return render(request, 'bookings.html', context)








# nexuspro/views.py (Locate and update the index view)

from .models import Testimonial # Ensure Testimonial is imported here

# ... (other view definitions) ...

def index(request):
    """Home Page - Now passes dynamically approved testimonials."""
    
    # Fetch only testimonials that have been approved by the Admin
    approved_testimonials = Testimonial.objects.filter(is_approved=True).order_by('-rating', '?')[:6]
    
    context = {
        'testimonials': approved_testimonials
    }
    return render(request, 'index.html', context)










#REGTEST

# nexuspro/views.py (TEMPORARY DEBUG VIEW)

def regtest(request):
    # ... (Keep form creation logic)
    if request.method == 'POST':
        # ... (POST logic)
        pass
    else:
        form = UserAndProfileCreationForm()
        
    context = {'form': form}
    
    # CRITICAL CHANGE: Use the DEBUG template
    return render(request, 'regtest.html', context) # <--- CHANGE TEMPLATE HERE


#ENDTESTREG