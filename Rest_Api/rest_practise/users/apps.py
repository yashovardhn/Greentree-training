from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        import users.signals
        # This imports the signals module to ensure that the signal handlers are registered
        # when the app is ready. This is necessary for the post_save signal to work correctly.
