from typing import Dict, Any
from BaseClasses import ItemClassification, Region
from worlds.AutoWorld import World

from .Items import OriBlindForestItem, base_items, keystone_items, mapstone_items, item_dict
from .Locations import location_list, all_trees, all_maps
from .Options import OriBlindForestOptions, LogicDifficulty, KeystoneLogic, MapstoneLogic, Goal
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

    def create_item(self, name: str) -> OriBlindForestItem:
        return OriBlindForestItem(name, item_dict[name][0], self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        placed_first_energy_cell = False

        item_list = dict(base_items)

        if self.options.keystone_logic == KeystoneLogic.option_area_specific:
            item_list = { **item_list, **keystone_items["AreaSpecific"] }
        else:
            item_list = { **item_list, **keystone_items["Anywhere"] }

        if self.options.mapstone_logic == MapstoneLogic.option_area_specific:
            item_list = { **item_list, **mapstone_items["AreaSpecific"] }
        else:
            item_list = { **item_list, **mapstone_items["Anywhere"] }

        for item_key, item_value in item_list.items():
            # override the item value for warmth fragments since it comes from options
            if item_key == "WarmthFragment" and self.options.goal == Goal.option_warmth_fragments:
                item_value = (item_value[0], self.options.warmth_fragments_available.value)

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

        # set the goal condition
        if self.options.goal == Goal.option_all_skill_trees:
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.can_reach_region("HoruEscapeInnerDoor", self.player) and \
                all(state.can_reach_location(skill_tree, self.player) for skill_tree in all_trees)
        elif self.options.goal == Goal.option_all_maps:
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.can_reach_region("HoruEscapeInnerDoor", self.player) and \
                all(state.can_reach_location(area_map, self.player) for area_map in all_maps)
        elif self.options.goal == Goal.option_warmth_fragments:
            # in case the required value is larger than the available, make the actual amount required equal to the available
            fragments_required: int = min(self.options.warmth_fragments_available.value, self.options.warmth_fragments_required.value)
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.can_reach_region("HoruEscapeInnerDoor", self.player) and \
                state.has("WarmthFragment", self.player, fragments_required)
        elif self.options.goal == Goal.option_none:
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.can_reach_region("HoruEscapeInnerDoor", self.player)

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "oribf_world.puml")

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}

        for option_name, option_value in self.options.as_dict():
            slot_data[option_name] = option_value

        return slot_data
