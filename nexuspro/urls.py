from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from nexuspro import views # Assumes all your views (functional and static) are here


urlpatterns = [
    # -----------------------------------------------------------
    # 1. ADMIN & STATIC PAGE VIEWS (No change, uses simple renders)
    # -----------------------------------------------------------



 path('admin/', admin.site.urls),

    path('', views.index, name ="index"),

    path('about/', views.about, name = "about"),

    path('base/', views.base, name ="base"),

    path('career/',views.career, name ="career"),

    path('contact/', views.contact, name ="contact"),

    path('network/', views.network, name ="network"),

    path('portfolio/', views.portfolio, name ="portfolio"),

    path('pricing/', views.pricing, name ="pricing"),

    path('privacy/',views.privacy, name ="privacy"),

    path('registration/', views.registration, name ="registration"),

    path('schedule/', views.schedule, name ="schedule"),

    path('security/', views.security,name ="security"),

    path('testimonials/', views.testimonials, name ="testimonials"),

    path('terms/', views.terms, name ="terms"),

    path('web/', views.web, name ="web"),



    path('bookings/', views.bookings, name ="bookings"),

    path('profile/', views.profile, name ="profile"),


    path('ccnp/', views.ccnp, name ="ccnp"),

    path('it/', views.it, name ="it"),

    path('technician/', views.technician, name ="technician"),

    path('editprofile/', views.editprofile, name ="edit_profile"),

 #TEST
  path('regtest/', views.regtest, name ="regtest"),



    path('admin/', admin.site.urls),
    path('', views.index, name ="index"),
    path('about/', views.about, name = "about"),
    path('contact/', views.contact, name ="contact"),
    path('network/', views.network, name ="network"),
    path('portfolio/', views.portfolio, name ="portfolio"),
    path('pricing/', views.pricing, name ="pricing"),
    path('privacy/', views.privacy, name ="privacy"),
    path('security/', views.security,name ="security"),
    path('testimonials/', views.testimonials, name ="testimonials"),
    path('terms/', views.terms, name ="terms"),
    path('web/', views.web, name ="web"),
    path('ccnp/', views.ccnp, name ="ccnp"),
    path('technician/', views.technician, name ="technician"),

    # NOTE: The 'base', 'career', 'registration', 'schedule', 'it', 'bookings' 
    #       placeholders were removed or should be mapped to functional views.

    # -----------------------------------------------------------
    # 2. AUTHENTICATION & ACCOUNT VIEWS (Functional)
    # -----------------------------------------------------------
    
    # 2a. Login (Uses built-in view with custom template)
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'), # <- This uses the correct view to pass the 'form' object!

    # 2b. Registration (Uses your functional view from views.py)
    path('register/', views.register_view, name ="register"), # <- MUST use register_view

    # 2c. Logout (Instant Redirect)
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/' 
    ), name='logout'),

    # 2d. Profile Dashboard (Functional View)
    path('profile/', views.profile_view, name ="profile"),
    
    # 2e. Edit Profile (Functional View)
    path('editprofile/', views.edit_profile_view, name ="edit_profile"),

    # 2f. Change Password (Built-in View, Corrected Template)
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html', # <- Corrected template name
        success_url='/profile/' 
    ), name='change_password'),
    
    # -----------------------------------------------------------
    # 3. PASSWORD RESET FLOW (Corrected URLs and Template Names)
    # -----------------------------------------------------------

    # 3a. Reset Form (Enter Email)
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url='/password-reset/done/' # <- Ensure leading slash for safety
    ), name='password_reset'),
    
    # 3b. Reset Done (Confirmation Email Sent)
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view( # Added trailing slash
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    
    # 3c. Reset Confirm (Set New Password via link)
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/password-reset/complete/' # <- Corrected URL path for consistency
    ), name='password_reset_confirm'),
    
    # 3d. Reset Complete (Success Message)
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]