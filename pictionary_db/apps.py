from django.apps import AppConfig


class PictionaryDbConfig(AppConfig):
    name = 'pictionary_db'

    def ready(self):
        from .models import Category, TempCategory
        while len(TempCategory.objects.all()) < 5:
            s = Category.objects.random()
            if not TempCategory.objects.filter(name=s).exists():
                TempCategory.objects.create(name=s)
