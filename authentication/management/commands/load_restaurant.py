import json
from django.core.management.base import BaseCommand
from main.models import Restaurant

class Command(BaseCommand):
    help = 'Load restaurant data from datasets.json into the database'

    def handle(self, *args, **kwargs):
        json_path = 'datasets/datasets.json'

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for restaurant_data in data['restaurants']:
            Restaurant.objects.create(
                name=restaurant_data['name'],
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded restaurant data'))