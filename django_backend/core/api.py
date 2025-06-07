from typing import List

from ninja_extra import NinjaExtraAPI

from .models import (
    GreaterPotion,
    LesserPotion,
    MagicItem,
    MagicWeaponOrArmour,
)
from .schemas import (
    GreaterPotionSchema,
    LesserPotionSchema,
    MagicItemSchema,
    MagicWeaponOrArmourSchema,
)

api = NinjaExtraAPI(
    version="1.0.0",
    title="Frostgrave Reborn API",
    description=(
        "API for Frostgrave Reborn, a management app for an indie tabletop wargame."
    ),
)


# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"


# --- New Endpoints for Listing All Items ---


@api.get("/greater_potion/list_all", response=List[GreaterPotionSchema], tags=["items"])
def list_greater_potions(request):
    """
    Retrieves a list of all Greater Potions from the database.
    """
    qs = GreaterPotion.objects.all()
    return qs


@api.get("/lesser_potion/list_all", response=List[LesserPotionSchema], tags=["items"])
def list_lesser_potions(request):
    """
    Retrieves a list of all Lesser Potions from the database.
    """
    qs = LesserPotion.objects.all()
    return qs


@api.get("/magic_item/list_all", response=List[MagicItemSchema], tags=["items"])
def list_magic_items(request):
    """
    Retrieves a list of all Magic Items from the database.
    """
    qs = MagicItem.objects.all()
    return qs


@api.get(
    "/magic_weapon_or_armour/list_all",
    response=List[MagicWeaponOrArmourSchema],
    tags=["items"],
)
def list_magic_weapons_or_armour(request):
    """
    Retrieves a list of all Magic Weapons or Armour from the database.
    """
    qs = MagicWeaponOrArmour.objects.all()
    return qs
