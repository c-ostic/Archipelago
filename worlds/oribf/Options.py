from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions

class Goal(Choice):
    """Choose the end goal.
    All Skill Trees: Find all 9 skill trees (excluding Kuro's feather) and finish Horu escape sequence."""
    display_name = "Goal"
    option_all_skill_trees = 0

class LogicDifficulty(Choice):
    """Sets the difficulty of the logic"""
    display_name = "Difficulty"
    option_casual = 0
    option_standard = 1
    option_expert = 2
    option_master = 3
    option_glitched = 4

class KeystoneLogic(Choice):
    """Choose how keystones can be used.
    Anywhere: All keystones can be used anywhere.
    Area Specific: Keystones are restricted to be used only in their given area."""
    display_name = "Keystone Logic"
    option_anywhere = 0
    option_area_specific = 1

class MapstoneLogic(Choice):
    """Choose how mapstones can be used.
    Anywhere: All mapstones can be used anywhere.
    Area Specific: Mapstones are restricted to be used only in their given area."""
    display_name = "Mapstone Logic"
    option_anywhere = 0
    option_area_specific = 1

class DeathLinkLogic(Choice):
    """Enable Death Link
    Disabled: Death Link is disabled
    Partial: Death Link is enabled, but will not send a death for any instant kill deaths.
    Full: Death Link is enabled, and will send for every death"""
    display_name = "Death Link"
    option_disabled = 0
    option_partial = 1
    option_full = 2

@dataclass
class OriBlindForestOptions(PerGameCommonOptions):
    goal: Goal
    logic_difficulty: LogicDifficulty
    keystone_logic: KeystoneLogic
    mapstone_logic: MapstoneLogic
    deathlink_logic: DeathLinkLogic
