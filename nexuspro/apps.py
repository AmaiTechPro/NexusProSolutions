# nexuspro/apps.py

from django.apps import AppConfig

class NexusproConfig(AppConfig):
    # Standard field used in newer Django versions
    default_auto_field = 'django.db.models.BigAutoField' 
    name = 'nexuspro'
    
    # CRITICAL FIX: The ready() method ensures signals are loaded when Django starts.
    def ready(self):
        # We import the signals file here, causing the receiver decorator to register 
        # the functions with Django's signal dispatch system.
        import nexuspro.signals