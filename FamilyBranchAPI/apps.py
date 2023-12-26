from django.apps import AppConfig


class FamilyBranchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FamilyBranch'

    def ready(self):
        import FamilyBranch.signals
