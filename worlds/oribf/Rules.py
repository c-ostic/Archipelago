from typing import Set, Dict

from .RulesData import location_rules, connection_rules
from BaseClasses import CollectionState, Region, Location, Entrance
from ..AutoWorld import World
from ..generic.Rules import add_rule


def apply_location_rules(world: World):
    # for each (valid) ruleset in location rules, call process_ruleset
    for ruleset_name, ruleset in location_rules.items():
        if ruleset_name in world.logic_sets:
            process_ruleset(world, ruleset, True)
    return


def apply_connection_rules(world: World):
    # for each region in connection rules, and for each (valid) ruleset under that region, call process_ruleset
    for region_name, rulesets in connection_rules.items():
        for ruleset_name, ruleset in rulesets.items():
            if ruleset_name in world.logic_sets:
                process_ruleset(world, ruleset, False, world.get_region(region_name))
    return


def process_ruleset(world: World, ruleset: Dict, is_location: bool, start_region: Region = None):
    # for each location or connecting region, call process_access_point
    # if location, forward the location
    # if connecting region, create and forward a new entrance
    for access_point_name, access_sets in ruleset.items():
        # TODO: might need to check if the location/region exists before trying to access
        access_point = None
        if is_location:
            access_point = world.get_location(access_point_name)
        else:
            access_point = start_region.connect(world.get_region(access_point_name))

        process_access_point(world, access_point, access_sets)
    return


def process_access_point(world: World, access_point: Location | Entrance, access_sets):
    # for each access set for the location/entrance, set a rule using oribf_has_all
    for access_set in access_sets:
        if "Free" not in access_set:
            add_rule(access_point, lambda state: oribf_has_all(state, access_set, world.player))
    return


def oribf_has_all(state: CollectionState, items: Set[str], player: int) -> bool:
    return all(state.has(item, player) if type(item) == str else state.has(item[0], player, int(item[1]))
               for item in items)
