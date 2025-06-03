# Copyright (C) Takeshi Nakamura. All rights reserved.

import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.encoding import force_str
from django.utils.translation import override
from django_countries.data import COUNTRIES

from wine.models import Wine

with override("en"):
    COUNTRY_MAP = {force_str(name): code for code, name in COUNTRIES.items()}


class Command(BaseCommand):
    help = "Import LWIN data converted to CSV."

    def add_arguments(self, parser):
        parser.add_argument("data_csv")

    def handle(self, *args, **options):
        with open(options["data_csv"], "r", encoding="utf-8") as f:
            objs = []
            reader = csv.DictReader(f)

            for row in reader:
                objs.append(Wine(
                    lwin=int(row["LWIN"]),
                    status=row["STATUS"],
                    display_name=row["DISPLAY_NAME"],
                    producer_title=_str(row["PRODUCER_TITLE"]),
                    producer_name=_str(row["PRODUCER_NAME"]),
                    wine=_str(row["WINE"]),
                    country=_country(row["COUNTRY"]),
                    region=_str(row["REGION"]),
                    sub_region=_str(row["SUB_REGION"]),
                    site=_str(row["SITE"]),
                    parcel=_str(row["PARCEL"]),
                    colour=str(row["COLOUR"]),
                    type=row["TYPE"],
                    sub_type=_str(row["SUB_TYPE"]),
                    designation=_str(row["DESIGNATION"]),
                    classification=_str(row["CLASSIFICATION"]),
                    vintage_config=row["VINTAGE_CONFIG"],
                    first_vintage=_vintage(row["FIRST_VINTAGE"]),
                    final_vintage=_vintage(row["FINAL_VINTAGE"]),
                    date_added=_datetime(row["DATE_ADDED"]),
                    date_updated=_datetime(row["DATE_UPDATED"]),
                ))

        Wine.objects.bulk_create(objs, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(
            "Successfully imported wine data."
        ))


def _str(value):
    return "" if value == "NA" else value


def _country(country_str):
    if country_str == "United States":
        return "US"

    return COUNTRY_MAP.get(country_str, "")


def _datetime(datetime_str):
    return datetime.strptime(f"{datetime_str}Z", "%Y-%m-%d %H:%M:%S%z")


def _vintage(vintage_str):
    return 0 if vintage_str == "NA" else int(vintage_str)
