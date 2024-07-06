from BaseClasses import Item, ItemClassification


class OriBlindForestItem(Item):
    game: str = "Ori and the Blind Forest"


item_dict = {
    "AbilityCell": (ItemClassification.progression, 33),
    "HealthCell": (ItemClassification.progression, 12),
    "EnergyCell": (ItemClassification.progression, 14),
    "KeyStone": (ItemClassification.progression, 40),
    "Plant": (ItemClassification.useful, 24),

    "MapStone": (ItemClassification.progression, 9),

    "GinsoKey": (ItemClassification.progression, 1),
    "ForlornKey": (ItemClassification.progression, 1),
    "HoruKey": (ItemClassification.progression, 1),
    "Wind": (ItemClassification.progression, 1),
    "CleanWater": (ItemClassification.progression, 1),

    "Bash": (ItemClassification.progression, 1),
    "ChargeFlame": (ItemClassification.progression, 1),
    "ChargeJump": (ItemClassification.progression, 1),
    "Climb": (ItemClassification.progression, 1),
    "Dash": (ItemClassification.progression, 1),
    "DoubleJump": (ItemClassification.progression, 1),
    "Glide": (ItemClassification.progression, 1),
    "Grenade": (ItemClassification.progression, 1),
    "Stomp": (ItemClassification.progression, 1),
    "WallJump": (ItemClassification.progression, 1),

    "EX15": (ItemClassification.filler, 6),
    "EX100": (ItemClassification.filler, 53),
    "EX200": (ItemClassification.filler, 29),

    # add some extra filler exp to compensate for map locations and horu room checks
    "EX50": (ItemClassification.filler, 17)
}
