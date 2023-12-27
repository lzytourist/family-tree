from django.apps import AppConfig


class FamilyBranchAPIConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FamilyBranchAPI'

    def ready(self):
        import FamilyBranch.signals
