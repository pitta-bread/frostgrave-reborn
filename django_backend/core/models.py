# Create your models here.
from django.db import models


class BaseItem(models.Model):
    """
    An abstract base class model that provides common fields
    for all game items.
    """

    name = models.CharField(max_length=255)
    purchase = models.PositiveIntegerField(
        null=True, blank=True, help_text="Price in gold coins (gc)"
    )
    sale = models.PositiveIntegerField(
        null=True, blank=True, help_text="Price in gold coins (gc)"
    )
    # the dice roll required to obtain this item
    die_roll = models.PositiveIntegerField(
        null=True, blank=True, help_text="Dice roll required to obtain this item"
    )

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class GreaterPotion(BaseItem):
    """
    Represents a Greater Potion item in the game.
    """

    ingredient_cost = models.PositiveIntegerField(null=True, blank=True)


class LesserPotion(BaseItem):
    """
    Represents a Lesser Potion item in the game.
    """

    pass  # This model only needs the common fields from BaseItem


class MagicItem(BaseItem):
    """
    Represents a Magic Item in the game.
    """

    pass  # This model only needs the common fields from BaseItem


class MagicWeaponOrArmour(BaseItem):
    """
    Represents a Magic Weapon or Armour item in the game.
    """

    effects = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Effect of the magic weapon or armour",
    )


class Treasure(models.Model):
    """
    Represents a Treasure result in the game.
    """

    die_roll = models.PositiveIntegerField(
        null=True, blank=True, help_text="Dice roll required to obtain this treasure"
    )
    gold = models.PositiveIntegerField(
        null=True, blank=True, help_text="Amount of gold coins (gc) in the treasure"
    )
    multiply_gold_by_d20 = models.BooleanField(
        default=False, help_text="Multiply the gold amount by a d20 roll"
    )
    result = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Description of the treasure result, in addition to the gold amount",
    )


class RandomSpell(models.Model):
    """
    Represents a Random Spell result in the game.
    """

    die_roll = models.PositiveIntegerField(
        null=True, blank=True, help_text="Dice roll required to obtain this spell"
    )
    second_die_1_to_5 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="If second die roll result is between 1 and 5, this happens",
    )
    second_die_6_to_10 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="If second die roll result is between 6 and 10, this happens",
    )
    second_die_11_to_15 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="If second die roll result is between 11 and 15, this happens",
    )
    second_die_16_to_20 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="If second die roll result is between 16 and 20, this happens",
    )
