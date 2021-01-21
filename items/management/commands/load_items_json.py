import json
from io import BytesIO

from django.core.management.base import BaseCommand, CommandError

from items.models import Item

import requests


class Command(BaseCommand):
    help = "Loads json and makes DB entities of Review model"

    def add_arguments(self, parser):
        parser.add_argument("--url", required=False)
        parser.add_argument("--path", required=False)

    def load_resource_from(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    def get_items_from_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.loads(file.read())

    def fill_db_from(self, items):
        for id, item in enumerate(items):
            self.stdout.write(self.style.NOTICE(f"processing {id+1} of {len(items)}"))
            try:
                new_item, _ = Item.objects.get_or_create(
                    title=item["title"],
                    description=item["description"],
                    weight=item["weight_grams"],
                    price=item["price"],
                )
                image_content = requests.get(item["image"]).content
                new_item.image.save(
                    item["image"].split("/")[-1], BytesIO(image_content), save=True
                )
            except Exception as e:
                self.stdout.write(self.style.NOTICE(e))

    def handle(self, *args, **options):
        try:
            if "url" not in options and "path" not in options:
                raise CommandError("Empty arguments")
            if "url" in options:
                items = self.load_resource_from(options["url"]).json()
            else:
                items = self.get_items_from_file(options["path"])
            self.fill_db_from(items)
        except BaseException as e:
            self.stdout.write(self.style.NOTICE(e))
            raise CommandError(e)
