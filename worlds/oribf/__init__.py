from BaseClasses import ItemClassification, Region
from worlds.AutoWorld import World

from .Items import OriBlindForestItem, item_dict
from .Locations import location_list, all_trees
from .Options import OriBlindForestOptions, LogicDifficulty
from .Rules import apply_location_rules, apply_connection_rules
from .Regions import region_list


class OriBlindForestWorld(World):
    # TODO: Make description
    """Insert description of the world/game here."""
    game = "Ori and the Blind Forest"
    options_dataclass = OriBlindForestOptions
    options: OriBlindForestOptions
    topology_present = True
    # TODO: Determine if this is a good number to use
    base_id = 262144
    item_name_to_id = {name: id for id, name in enumerate(item_dict, base_id)}
    location_name_to_id = {name: id for id, name in enumerate(location_list, base_id)}

    logic_sets = {}

    def generate_early(self):
        logic_sets = {"casual"} # always include at least casual

        if self.options.logic_difficulty == LogicDifficulty.option_glitched:
            logic_sets.add("glitched")
            logic_sets.add("master")
            logic_sets.add("expert")
            logic_sets.add("standard")
        
        if self.options.logic_difficulty == LogicDifficulty.option_master:
            logic_sets.add("master")
            logic_sets.add("expert")
            logic_sets.add("standard")

        if self.options.logic_difficulty == LogicDifficulty.option_expert:
            logic_sets.add("expert")
            logic_sets.add("standard")

        if self.options.logic_difficulty == LogicDifficulty.option_standard:
            logic_sets.add("standard")

        self.logic_sets = logic_sets

    def create_region(self, name: str):
        return Region(name, self.player, self.multiworld)

    def create_regions(self) -> None:
        menu = self.create_region("Menu")
        self.multiworld.regions.append(menu)

        for region_name in region_list:
            region = self.create_region(region_name)
            self.multiworld.regions.append(region)

            # set the starting region
            if region_name == "SunkenGladesRunaway":
                menu.connect(region)

        apply_connection_rules(self)
        apply_location_rules(self)

    def create_item(self, item: str) -> OriBlindForestItem:
        return OriBlindForestItem(item, item_dict[item][0], self.item_name_to_id[item], self.player)

    def create_items(self) -> None:
        placed_first_energy_cell = False

        for item_key, item_value in item_dict.items():
            for count in range(item_value[1]):
                item = self.create_item(item_key)
                self.multiworld.itempool.append(item)

                # place the first energy cell at its normal location so the player can save right away
                if item_key == "EnergyCell" and not placed_first_energy_cell:
                    self.get_location("FirstEnergyCell").place_locked_item(item)
                    placed_first_energy_cell = True

                

    def create_event(self, event: str) -> OriBlindForestItem:
        return OriBlindForestItem(event, ItemClassification.progression, None, self.player)

    def set_rules(self) -> None:
        # most of the rules are set above in create_regions
        self.multiworld.completion_condition[self.player] = lambda state: \
            state.can_reach_region("HoruEscapeInnerDoor", self.player) and \
            all(state.can_reach_location(skill_tree, self.player) for skill_tree in all_trees)

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "oribf_world.puml")
