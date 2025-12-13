
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

# nexuspro/views.py (Final context change)




#TEST2-PROFILE VIEW

# nexuspro/views.py (Focus on profile_view)

@login_required
def profile_view(request):
    # CRITICAL: Ensures the user_profile object exists
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    bookings = Booking.objects.filter(user=request.user).order_by('-request_date')

    context = {
        'bookings': bookings,
        'user_profile': user_profile, 
        'user': request.user 
    }
    
    # === TEMPORARY CRASH/DEBUG LINE (Add this) ===
    # This will print the database data for the user_profile object.
    # If the data is correct here, the issue is 100% in the template.
    print("--- DEBUG PROFILE DATA ---")
    print("Phone Number:", user_profile.phone_number)
    print("Service Interest:", user_profile.service_interest)
    print("Bio:", user_profile.bio)
    print("--------------------------")
    # raise Exception("STOP HERE") # Uncomment this line to force a crash if needed
    # ============================================

    return render(request, 'profile.html', context)




#ENDTEST PROFILE VIEW













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
            return redirect('edit_profile') 
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












# M-PESA API INTEGRATION

# nexuspro/views.py (Add new imports at the top)
import requests
import base64
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect # (ensure these are already there)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# --- M-PESA UTILITY FUNCTION ---

def get_mpesa_access_token():
    """Retrieves the M-Pesa API access token required for all transaction requests."""
    
    credentials = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
    # Base64 encode the key:secret pair
    auth_header = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    url = f"{settings.MPESA_API_BASE_URL}oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(
            url,
            headers={"Authorization": f"Basic {auth_header}"}
        )
        response.raise_for_status() 
        token_data = response.json()
        return token_data.get('access_token')
        
    except requests.exceptions.RequestException as e:
        # In a real app, you would log this error securely
        print(f"M-Pesa Token Error: {e}") 
        return None

# --- M-PESA TRANSACTION VIEWS ---

@login_required
def initiate_stk_push(request, amount, phone_number, account_reference="NexusProPayment"):
    """
    Initiates an STK Push payment prompt to the user's phone.
    
    Note: 'phone_number' must be in 2547XXXXXXXX format.
    """
    
    token = get_mpesa_access_token()
    if not token:
        messages.error(request, "Payment service temporarily unavailable (Authentication failure).")
        return redirect('profile') 

    # 1. Prepare Timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # 2. Prepare Password (Shortcode + Passkey + Timestamp)
    password_data = f"{settings.MPESA_SHORTCODE_STK}{settings.MPESA_PASSKEY}{timestamp}"
    password = base64.b64encode(password_data.encode('utf-8')).decode('utf-8')
    
    # 3. Define the API Request Body
    
    # CRITICAL FIX FOR TESTING: Hardcode the active Ngrok HTTPS URL
    # Replace the Ngrok URL below with your currently running one (it changes when Ngrok restarts)
    callback_url = "https://hegemonical-tensorial-felicita.ngrok-free.dev/mpesa/callback/"

    # Original line (DEACTIVATED FOR TESTING):
    # callback_url = request.build_absolute_uri('/mpesa/callback/') 

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE_STK,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline", 
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE_STK,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": "Service Payment - NexusPro"
    }

    # 4. Make the STK Push Request
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    stk_url = f"{settings.MPESA_API_BASE_URL}stkpush/v1/processrequest"
    
    try:
        response = requests.post(stk_url, json=payload, headers=headers)
        response.raise_for_status()
        
        stk_response = response.json()
        
        # Check M-Pesa's specific ResponseCode for success
        if stk_response.get("ResponseCode") == "0":
            # Successfully requested the prompt on the user's phone
            messages.success(request, "M-Pesa payment prompt sent successfully! Check your phone.")
        else:
            # Handle M-Pesa API errors (e.g., invalid phone number)
            messages.error(request, f"M-Pesa Request Error: {stk_response.get('ResponseDescription', 'Unknown API error')}")

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Failed to connect to M-Pesa service. Please try again.")

    return redirect('profile') # Redirect user back to profile dashboard


@csrf_exempt # Required because M-Pesa is an external POSTing to our server
def mpesa_callback(request):
    """
    Receives M-Pesa STK Push results (success or failure) from Safaricom.
    THIS MUST BE PUBLICLY ACCESSIBLE VIA HTTPS.
    """
    if request.method == 'POST':
        try:
            # Safaricom sends data as JSON in the request body
            callback_data = request.body.decode('utf-8')
            
            # CRITICAL: Log this data to a file/database for auditing!
            print("--- M-Pesa Callback Received ---")
            print(callback_data)
            
            # TODO: Add logic here to parse the JSON and update your Booking/Payment model
            # e.g., if ResultCode is 0, mark the booking as paid.

            # M-Pesa requires a specific JSON response to confirm receipt
            return JsonResponse({"ResultCode": 0, "ResultDesc": "C2B_Request_Received"}, status=200)

        except Exception as e:
            # Log errors during internal processing
            print(f"Error processing M-Pesa callback: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Internal_Error"}, status=500)
    
    return JsonResponse({"error": "Invalid method"}, status=405)

#END OF M-PESA API INTEGRATION