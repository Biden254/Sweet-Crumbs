from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Defer DB operations until after migrations
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver
        from .models import SiteConfig

        @receiver(post_migrate)
        def ensure_site_config(sender, **kwargs):
            try:
                if not SiteConfig.objects.exists():
                    SiteConfig.objects.create(llm_enabled=True)
            except Exception:
                pass