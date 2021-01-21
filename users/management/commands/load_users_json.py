import json
from io import BytesIO

from django.core.management.base import BaseCommand, CommandError

from users.models import User

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

    def get_users_from_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.loads(file.read())

    def fill_db_from(self, items):
        for id, item in enumerate(items):
            self.stdout.write(self.style.NOTICE(f"processing {id+1} of {len(items)}"))
            try:
                new_user, _ = User.objects.get_or_create(
                    password=item["password"],
                    last_name=item["info"]["surname"],
                    first_name=item["info"]["name"],
                    middle_name=item["info"]["patronymic"],
                    phone_number=item["contacts"]["phoneNumber"],
                    address=item["city_kladr"],
                    email=item["email"],
                )
                new_user.save()
            except Exception as e:
                self.stdout.write(self.style.NOTICE(e))

    def handle(self, *args, **options):
        try:
            if "url" not in options and "path" not in options:
                raise CommandError("Empty arguments")
            if "url" in options:
                users = self.load_resource_from(options["url"]).json()
            else:
                users = self.get_users_from_file(options["path"])
            self.fill_db_from(users)
        except BaseException as e:
            self.stdout.write(self.style.NOTICE(e))
            raise CommandError(e)
