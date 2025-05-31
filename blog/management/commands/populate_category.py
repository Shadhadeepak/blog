from typing import Any
from blog.models import Category
from django.core.management.base import BaseCommand  


class Command(BaseCommand):  # 
    help = 'This is used to populate Catergory data'

    def handle(self, *args: Any, **options: Any):
        #Delete exinting data
        Category.objects.all().delete()

        categories=[
            'sports',
            'Technology',
            "science",
            'Art',
            "Food"
        ]
        for category_name in categories:
            Category.objects.create(name=category_name)

        self.stdout.write(self.style.SUCCESS("✅ Successfully populated Post data"))
