from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
    
    def ready(self):
        logger.warning("POLLS APPS LOADED,tyaga lang at tiwala sa sarili palagi nothing impossible boss hehe!🔥")
        """
        Import signals when Django starts.
        
        Best Practice:
        - Signals are imported in ready() method
        - Ensures signals are registered before any code runs
        - Required for production deployment
        """
        import polls.signals  # noqa: F401
