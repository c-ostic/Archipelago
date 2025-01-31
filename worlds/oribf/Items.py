from BaseClasses import Item, ItemClassification


class OriBlindForestItem(Item):
    game: str = "Ori and the Blind Forest"


base_items = {
    "AbilityCell": (ItemClassification.progression, 33),
    "HealthCell": (ItemClassification.progression, 12),
    "EnergyCell": (ItemClassification.progression, 14),

    "GinsoKey": (ItemClassification.progression, 1),
    "ForlornKey": (ItemClassification.progression, 1),
    "HoruKey": (ItemClassification.progression, 1),
    "CleanWater": (ItemClassification.progression, 1),
    "Wind": (ItemClassification.progression, 1),

    "WallJump": (ItemClassification.progression, 1),
    "ChargeFlame": (ItemClassification.progression, 1),
    "DoubleJump": (ItemClassification.progression, 1),
    "Bash": (ItemClassification.progression, 1),
    "Stomp": (ItemClassification.progression, 1),
    "Glide": (ItemClassification.progression, 1),
    "Climb": (ItemClassification.progression, 1),
    "ChargeJump": (ItemClassification.progression, 1),
    "Dash": (ItemClassification.progression, 1),
    "Grenade": (ItemClassification.progression, 1),

    "TPGlades": (ItemClassification.progression, 1),
    "TPGrove": (ItemClassification.progression, 1),
    "TPSwamp": (ItemClassification.progression, 1),
    "TPGrotto": (ItemClassification.progression, 1),
    "TPGinso": (ItemClassification.progression, 1),
    "TPValley": (ItemClassification.progression, 1),
    "TPForlorn": (ItemClassification.progression, 1),
    "TPSorrow": (ItemClassification.progression, 1),
    "TPHoru": (ItemClassification.progression, 1),
    "TPBlackroot": (ItemClassification.progression, 1),

    "WarmthFragment": (ItemClassification.progression, 0),
    "Relic": (ItemClassification.progression, 0)
}

keystone_items = {
    "Anywhere" : {
        "KeyStone": (ItemClassification.progression, 40)
    },
    "AreaSpecific" : {
        "GladesKeyStone": (ItemClassification.progression, 8),
        "GrottoKeyStone": (ItemClassification.progression, 2),
        "GinsoKeyStone": (ItemClassification.progression, 8),
        "SwampKeyStone": (ItemClassification.progression, 2),
        "MistyKeyStone": (ItemClassification.progression, 4),
        "ForlornKeyStone": (ItemClassification.progression, 4),
        "SorrowKeyStone": (ItemClassification.progression, 12)
    }
}

mapstone_items = {
    "Anywhere" : {
        "MapStone": (ItemClassification.progression, 9),
    },
    "AreaSpecific" : {
        "GladesMapStone": (ItemClassification.progression, 1),
        "GroveMapStone": (ItemClassification.progression, 1),
        "GrottoMapStone": (ItemClassification.progression, 1),
        "SwampMapStone": (ItemClassification.progression, 1),
        "ValleyMapStone": (ItemClassification.progression, 1),
        "ForlornMapStone": (ItemClassification.progression, 1),
        "SorrowMapStone": (ItemClassification.progression, 1),
        "HoruMapStone": (ItemClassification.progression, 1),
        "BlackrootMapStone": (ItemClassification.progression, 1)
    }
}

filler_items = {
    # since filler is added dynamically at the end of item generation, the numbers here don't correspond
    # with how many are in the multiworld. Rather they are weights relative to each other
    "EX15": (ItemClassification.filler, 2),
    "EX50": (ItemClassification.filler, 3),
    "EX100": (ItemClassification.filler, 4),
    "EX200": (ItemClassification.filler, 2)
}

item_dict = {
    **base_items,
    **keystone_items["Anywhere"],
    **keystone_items["AreaSpecific"],
    **mapstone_items["Anywhere"],
    **mapstone_items["AreaSpecific"],
    **filler_items
}

item_alias_list = {
    "KurosFeather": {"Glide"},
    "LightBurst": {"Grenade"},
    "WaterVein": {"GinsoKey"},
    "GumonSeal": {"ForlornKey"},
    "Sunstone": {"HoruKey"}
}