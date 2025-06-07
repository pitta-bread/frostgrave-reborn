from ninja import ModelSchema

from .models import (
    GreaterPotion,
    LesserPotion,
    MagicItem,
    MagicWeaponOrArmour,
)

# By using fields = '__all__', the schema will automatically expose
# all fields from the corresponding model. This is much more maintainable.


class GreaterPotionSchema(ModelSchema):
    class Meta:
        model = GreaterPotion
        fields = "__all__"


class LesserPotionSchema(ModelSchema):
    class Meta:
        model = LesserPotion
        fields = "__all__"


class MagicItemSchema(ModelSchema):
    class Meta:
        model = MagicItem
        fields = "__all__"


class MagicWeaponOrArmourSchema(ModelSchema):
    class Meta:
        model = MagicWeaponOrArmour
        fields = "__all__"
