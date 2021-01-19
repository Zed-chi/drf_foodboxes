import json
from io import BytesIO

from django.core.management.base import BaseCommand, CommandError

from items.models import Item

import requests


class Command(BaseCommand):
    help = "Loads json and makes DB entities of Review model"

    def add_arguments(self, parser):
        parser.add_argument("url")
        parser.add_argument("path")

    def load_resource_from(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    def get_reviews_from_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.loads(file.read())

    def fill_db_from(self, items):
        for item in items:
            new_item, _ = Item.objects.get_or_create(
                title=item["title"],
                description=item["description"],
                weight=item["weight_grams"],
                price=item["price"],
            )
            image_content = requests.get(item["image"]).content
            new_item.image.save(
                item["title"], BytesIO(image_content), save=True
            )
        return

    def handle(self, *args, **options):
        try:
            if "url" not in options and "path" not in options:
                return
            if "url" in options:
                reviews = self.load_resource_from(options["url"]).json()
            else:
                reviews = self.get_reviews_from_file(options["path"])
            self.fill_db_from(reviews)
        except BaseException as e:
            self.stdout.write(self.style.NOTICE(e))
            raise CommandError(e)
