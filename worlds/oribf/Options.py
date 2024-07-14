from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions


class LogicDifficulty(Choice):
    """Sets the difficulty of the logic"""
    display_name = "Difficulty"
    option_casual = 0
    option_standard = 1
    option_expert = 2
    option_master = 3
    option_glitched = 4


@dataclass
class OriBlindForestOptions(PerGameCommonOptions):
    logic_difficulty: LogicDifficulty
