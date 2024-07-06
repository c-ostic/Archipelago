from dataclasses import dataclass

from Options import Toggle, PerGameCommonOptions


class DummyTest(Toggle):
    """Dummy option."""
    display_name = "Test"


@dataclass
class OriBlindForestOptions(PerGameCommonOptions):
    dummyTest: DummyTest
