import json
from django.core.management.base import BaseCommand
from main.models import Restaurant, Menu

class Command(BaseCommand):
    help = 'Load restaurant data from datasets.json into the database'

    def handle(self, *args, **kwargs):
        json_path = 'datasets/datasets.json'

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for restaurant_data in data['restaurants']:
            restaurant = Restaurant.objects.create(
                name=restaurant_data['name'],
            )

            # Loop through the menu items and create Menu instances
            for menu_item in restaurant_data['menu']:
                Menu.objects.create(
                    restaurant=restaurant,
                    food_name=menu_item['food_name'],
                    price=menu_item['price'],
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded restaurant and menu data'))
