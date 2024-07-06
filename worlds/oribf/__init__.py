from BaseClasses import ItemClassification, Region
from worlds.AutoWorld import World

from .Items import OriBlindForestItem, item_dict
from .Locations import OriBlindForestLocation, location_list, all_trees
from .Options import OriBlindForestOptions
from .Rules import apply_location_rules, apply_connection_rules
from .Regions import locations_by_region, connectors


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
        logic_sets = {"casual-core"}
        # TODO: Add options for other logic sets
        self.logic_sets = logic_sets

    def create_region(self, name: str):
        return Region(name, self.player, self.multiworld)

    def create_regions(self) -> None:
        menu = self.create_region("Menu")
        self.multiworld.regions.append(menu)

        # create regions and assign locations
        already_placed_locations = set()

        for region_name, locations in locations_by_region.items():
            locations -= already_placed_locations
            already_placed_locations |= locations
            region = self.create_region(region_name)
            region.add_locations({location: self.location_name_to_id[location] for location in locations},
                                 OriBlindForestLocation)
            self.multiworld.regions.append(region)

            # set the starting region
            if region_name == "SunkenGladesRunaway":
                menu.connect(region)

        apply_connection_rules(self)

        # go through all other connections and add any free connections that were otherwise unspecified in the rules
        for region_name, connections in connectors.items():
            region = self.get_region(region_name)
            existing_connections = []
            for exit in region.exits:
                existing_connections.append(exit.connected_region)

            for connecting_region in connections:
                if connecting_region not in existing_connections:
                    region.connect(self.get_region(connecting_region))

    def create_item(self, item: str) -> OriBlindForestItem:
        return OriBlindForestItem(item, item_dict[item][0], self.item_name_to_id[item], self.player)

    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            for count in range(item_value[1]):
                self.multiworld.itempool.append(self.create_item(item_key))

    def create_event(self, event: str) -> OriBlindForestItem:
        return OriBlindForestItem(event, ItemClassification.progression, None, self.player)

    def set_rules(self) -> None:
        apply_location_rules(self)

        self.get_location("HoruEscape").place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player) and \
            all(state.can_reach_location(skill_tree, self.player) for skill_tree in all_trees)

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "oribf_world.puml")
