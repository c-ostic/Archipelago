from dataclasses import dataclass

from Options import Toggle, Choice, Range, PerGameCommonOptions

class Goal(Choice):
    """Choose the end goal. All goals determine what unlocks the final Horu escape sequence
    All Skill Trees: Find all 10 skill trees (including Kuro's feather)
    All Maps: Place all 9 mapstones around the map
    Warmth Fragments: Collect the required number of Warmth Fragments
    World Tour: Collect the required number of Relics. Up to 11 areas (default 8) around Nibel will be chosen to contain a relic in a random location
    None: No extra conditions, just reach and finish the final escape
    """
    display_name = "Goal"
    option_all_skill_trees = 0
    option_all_maps = 1
    option_warmth_fragments = 2
    option_world_tour = 3
    option_none = 4
    default = 0

class WarmthFragmentsAvailable(Range):
    """The number of Warmth Fragments that exist"""
    display_name = "Warmth Fragments Available"
    range_start = 1
    range_end = 50
    default = 30

class WarmthFragmentsRequired(Range):
    """The number of Warmth Fragments needed for the goal"""
    display_name = "Warmth Fragments Required"
    range_start = 1
    range_end = 50
    default = 20

class RelicCount(Range):
    """The number of areas chosen to contain Relics"""
    display_name = "Relic Count"
    range_start = 1
    range_end = 11
    default = 8

class LogicDifficulty(Choice):
    """Sets the difficulty of the logic"""
    display_name = "Difficulty"
    option_casual = 0
    option_standard = 1
    option_expert = 2
    option_master = 3
    option_glitched = 4
    default = 0

class KeystoneLogic(Choice):
    """Choose how keystones can be used.
    Anywhere: All keystones can be used anywhere.
    Area Specific: Keystones are restricted to be used only in their given area."""
    display_name = "Keystone Logic"
    option_anywhere = 0
    option_area_specific = 1
    default = 0

class MapstoneLogic(Choice):
    """Choose how mapstones can be used.
    Anywhere: All mapstones can be used anywhere.
    Area Specific: Mapstones are restricted to be used only in their given area.
    Progressive: Similar to anywhere, but it doesn't matter where the mapstone is used.
        The first mapstone used will always send ProgressiveMapstone1 and the last will send ProgressiveMapstone9"""
    display_name = "Mapstone Logic"
    option_anywhere = 0
    option_area_specific = 1
    option_progressive = 2
    default = 0

class ExtraMapstones(Range):
    """Adds extra mapstones to the pool to make it easier to get the 9 required. Affects anywhere and progressive mapstone logic"""
    display_name = "Extra Mapstones"
    range_start = 0
    range_end = 9
    default = 0

class DeathLinkLogic(Choice):
    """Enable Death Link
    Disabled: Death Link is disabled
    Partial: Death Link is enabled, but will not send a death for any instant kill deaths.
    Full: Death Link is enabled, and will send for every death"""
    display_name = "Death Link"
    option_disabled = 0
    option_partial = 1
    option_full = 2
    default = 0

class EnableLure(Toggle):
    """Allows luring enemies to be considered for logic. Affects standard and above, 
    but higher difficulties may require more difficult lures."""
    display_name = "Enable Lure"
    default = 1

class EnableDamageBoost(Toggle):
    """Allows taking damage to be considered for logic. Affects all difficulties, but higher difficulties may require more damage. 
    Use of Ultra Defense ability limited to master. At least 12 ability cells will be in logic before needing to use this ability."""
    display_name = "Enable Damage Boost"
    default = 1

class EnableDoubleBash(Toggle):
    """Allows double bash technique to be considered for logic. Affects expert and above."""
    display_name = "Enable Double Bash"
    default = 1

class EnableGrenadeJump(Toggle):
    """Allows grenade jump technique to be considered for logic. Affects master."""
    display_name = "Enable Grenade Jump"
    default = 1

class EnableAirDash(Toggle):
    """Allows air dash ability to be considered for logic. Affects standard and above. 
    At least 3 ability cells will be in logic before needing to use this ability."""
    display_name = "Enable Air Dash"
    default = 1

class EnableChargeDash(Toggle):
    """Allows charge dash ability to be considered for logic. Affects expert and above. 
    At least 6 ability cells will be in logic before needing to use this ability."""
    display_name = "Enable Charge Dash"
    default = 1

class EnableTripleJump(Toggle):
    """Allows triple jump ability to be considered for logic. Only affects master. 
    At least 12 ability cells will be in logic before needing to use this ability."""
    display_name = "Enable Triple Jump"
    default = 1

class EnableChargeFlameBurn(Toggle):
    """Allows charge flame burn ability to be considered for logic. Only affects master. 
    At least 3 ability cells will be in logic before needing to use this ability."""
    display_name = "Enable Charge Flame Burn"
    default = 1

class EnableRekindle(Toggle):
    """Allows rekindle ability to be considered for logic. Only affects standard, expert, and master
    for specifically the Ghost Lever trick in Blackroot Burrows"""
    display_name = "Enable Rekindle"
    default = 1

class RestrictDungeonKeys(Toggle):
    """Due to teleporters, it is possible for dungeon keys (ex. GinsoKey) to end up placed inside 
    their dungeon. This option prevents those keys from being placed there"""
    display_name = "Restrict Dungeon Keys"
    default = 0

@dataclass
class OriBlindForestOptions(PerGameCommonOptions):
    goal: Goal
    warmth_fragments_available: WarmthFragmentsAvailable
    warmth_fragments_required: WarmthFragmentsRequired
    relic_count: RelicCount
    logic_difficulty: LogicDifficulty
    keystone_logic: KeystoneLogic
    mapstone_logic: MapstoneLogic
    extra_mapstones: ExtraMapstones
    deathlink_logic: DeathLinkLogic
    enable_lure: EnableLure
    enable_damage_boost: EnableDamageBoost
    enable_double_bash: EnableDoubleBash
    enable_grenade_jump: EnableGrenadeJump
    enable_air_dash: EnableAirDash
    enable_charge_dash: EnableChargeDash
    enable_triple_jump: EnableTripleJump
    enable_charge_flame_burn: EnableChargeFlameBurn
    enable_rekindle: EnableRekindle
    restrict_dungeon_keys: RestrictDungeonKeys

slot_data_options: list[str] = [
    "goal",
    "warmth_fragments_available",
    "warmth_fragments_required",
    "relic_count",
    "logic_difficulty",
    "keystone_logic",
    "mapstone_logic",
    "deathlink_logic",
    "enable_lure",
    "enable_damage_boost",
    "enable_double_bash",
    "enable_grenade_jump",
    "enable_air_dash",
    "enable_charge_dash",
    "enable_triple_jump",
    "enable_charge_flame_burn",
    "enable_rekindle"
]
