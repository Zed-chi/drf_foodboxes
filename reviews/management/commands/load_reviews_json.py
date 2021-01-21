import json
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

import requests

from reviews.models import Review


class Command(BaseCommand):
    help = "Loads json and makes DB entities of Review model"

    def add_arguments(self, parser):
        parser.add_argument("--url", required=False)
        parser.add_argument("--path", required=False)

    def load_resource_from(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    def get_reviews_from_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.loads(file.read())

    def fill_db_from(self, items):
        for id, item in enumerate(items):
            self.stdout.write(self.style.NOTICE(f"processing {id+1} of {len(items)}"))
            try:
                new_review, _ = Review.objects.get_or_create(
                    author=item["author"],
                    text=item["text"],
                    created_at=datetime.strptime(
                        item["created_at"], "%y-%d-%m"
                    ),
                    published_at=datetime.strptime(
                        item["published_at"], "%y-%d-%m"
                    ),
                    status=item["status"],
                )
                new_review.save()
            except Exception as e:
                self.stdout.write(self.style.NOTICE(e))

    def handle(self, *args, **options):
        try:
            if "url" not in options and "path" not in options:
                raise CommandError("Empty arguments")
            if "url" in options:
                reviews = self.load_resource_from(options["url"]).json()
            else:
                reviews = self.get_reviews_from_file(options["path"])
            self.fill_db_from(reviews)
        except BaseException as e:
            self.stdout.write(self.style.NOTICE(e))
            raise CommandError(e)
