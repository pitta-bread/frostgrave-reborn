# core/management/commands/load_items.py

import csv

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError


def to_int_or_none(value):
    """
    Helper function to safely convert a string to an integer.
    Returns None if the string is empty or invalid.
    """
    if value is None or value == "":
        return None
    try:
        return int(value.replace(",", ""))
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = (
        "Loads item data from a specified CSV file into a specified item model. "
        "Uses 'die_roll' as the unique key for each item."
    )

    # A mapping of the user-friendly item type argument to the actual model class name.
    MODEL_MAP = {
        "greaterpotion": "GreaterPotion",
        "lesserpotion": "LesserPotion",
        "magicitem": "MagicItem",
        "magicweaponorarmour": "MagicWeaponOrArmour",
    }

    def add_arguments(self, parser):
        """
        Define the command-line arguments the command will accept.
        """
        parser.add_argument(
            "item_type",
            choices=self.MODEL_MAP.keys(),
            help="The type of item to load (e.g., 'magicweaponorarmour').",
        )
        parser.add_argument(
            "csv_file_path",
            type=str,
            help="The full path to the CSV file containing the item data.",
        )

    def handle(self, *args, **options):
        """
        The main logic of the command.
        """
        item_type_key = options["item_type"].lower()
        csv_file_path = options["csv_file_path"]

        model_name = self.MODEL_MAP.get(item_type_key)
        if not model_name:
            raise CommandError(f"Invalid item type '{item_type_key}'.")

        # Dynamically get the model class from your app (assuming app is named 'core')
        # Change 'core' to the actual name of your app if it's different.
        try:
            ItemModel = apps.get_model("core", model_name)
        except LookupError:
            raise CommandError(
                f"Model '{model_name}' not found in app 'core'. "
                "Is your app name correct?"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"--- Starting import for model '{model_name}' from '{
                    csv_file_path
                }' ---"
            )
        )

        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                # Check if required headers are in the CSV
                required_headers = ["die_roll", "name", "purchase", "sale"]
                if not all(header in reader.fieldnames for header in required_headers):
                    raise CommandError(
                        f"CSV file must contain the following headers: {
                            ', '.join(required_headers)
                        }"
                    )

                created_count = 0
                updated_count = 0

                for row in reader:
                    die_roll_val = to_int_or_none(row.get("die_roll"))
                    if die_roll_val is None:
                        self.stderr.write(
                            self.style.WARNING(
                                f"Skipping row with invalid or missing 'die_roll': {
                                    row
                                }"
                            )
                        )
                        continue

                    # Use die_roll as the unique identifier for the lookup.
                    lookup_fields = {"die_roll": die_roll_val}

                    # Prepare the data dictionary with all other fields for
                    # creating/updating.
                    defaults = {
                        "name": row.get("name", ""),
                        "purchase": to_int_or_none(row.get("purchase")),
                        "sale": to_int_or_none(row.get("sale")),
                    }

                    # Add model-specific fields to the defaults dictionary
                    if model_name == "MagicWeaponOrArmour":
                        defaults["effects"] = row.get("effects", "")
                    elif model_name == "GreaterPotion":
                        defaults["ingredient_cost"] = to_int_or_none(
                            row.get("ingredient_cost")
                        )

                    try:
                        obj, created = ItemModel.objects.update_or_create(
                            **lookup_fields, defaults=defaults
                        )
                        display_name = (
                            defaults.get("name") or f"Item with Die Roll {die_roll_val}"
                        )
                        if created:
                            created_count += 1
                            self.stdout.write(f"  Created: {display_name}")
                        else:
                            updated_count += 1
                            self.stdout.write(f"  Updated: {display_name}")

                    except IntegrityError as e:
                        self.stderr.write(
                            self.style.ERROR(
                                f"Could not process row due to an integrity error: {
                                    row
                                }. Error: {e}"
                            )
                        )
                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(
                                f"An unexpected error occurred for row: {row}. Error: {
                                    e
                                }"
                            )
                        )

        except FileNotFoundError:
            raise CommandError(
                f'File not found at "{csv_file_path}". Please check the path.'
            )
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {e}")

        self.stdout.write(
            self.style.SUCCESS(
                f"--- Import finished: {created_count} created, {
                    updated_count
                } updated. ---"
            )
        )
