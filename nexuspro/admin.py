# nexuspro/admin.py

from django.contrib import admin
# Ensure all your models are imported from your local models.py
from .models import Appointment, Booking, Profile, Testimonial, Register 

# ----------------------------------------------------------------------
# 1. Custom Admin Class for Testimonials (Using the decorator)
# ----------------------------------------------------------------------

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    # Fields displayed in the list view of the admin page
    list_display = ('client_name', 'service_provided', 'rating', 'is_approved', 'user')
    
    # Fields that can be filtered on the right sidebar
    list_filter = ('is_approved', 'service_provided', 'rating')
    
    # Fields that can be searched
    search_fields = ('client_name', 'quote')
    
    # Actions that can be performed on selected testimonials
    actions = ['make_approved', 'make_unapproved']
    
    # Custom action to quickly approve testimonials
    @admin.action(description='Mark selected testimonials as approved')
    def make_approved(self, request, queryset):
        queryset.update(is_approved=True)

    # Custom action to quickly unapprove testimonials
    @admin.action(description='Mark selected testimonials as unapproved')
    def make_unapproved(self, request, queryset):
        queryset.update(is_approved=False)

# ----------------------------------------------------------------------
# 2. Basic Registrations (Using admin.site.register for simpler models)
# ----------------------------------------------------------------------

# Register the Profile model
admin.site.register(Profile)

# Register the Booking model
admin.site.register(Booking)

# Register the Register model (Assuming this is an old or temporary model.
# If you fully moved to Django's built-in User/Profile, you might want to delete this later.)
admin.site.register(Register)
admin.site.register(Appointment)