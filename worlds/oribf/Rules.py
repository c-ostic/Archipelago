from typing import Set

from .RulesData import location_rules, connection_rules
from .Items import item_dict
from .Locations import OriBlindForestLocation
from BaseClasses import CollectionState, Location, Entrance
from ..AutoWorld import World
from ..generic.Rules import add_rule, set_rule


def apply_location_rules(world: World):
    # for each region in location rules, and for each location
    # create a location and call process_access_point
    for region_name, locations in location_rules.items():
        region = world.get_region(region_name)
        region.add_locations({location: world.location_name_to_id[location] for location in locations}, OriBlindForestLocation)

        for location, rulesets in locations.items():
            process_access_point(world, world.get_location(location), rulesets)


def apply_connection_rules(world: World):
    # for each region in connection rules, and for each connecting region, 
    # create an entrance and call process_access_point
    for region_name, connections in connection_rules.items():
        region = world.get_region(region_name)
        id = 1
        for connection, rulesets in connections.items():
            entrance_name = region_name + "_to_" + connection + "_" + str(id)
            id += 1
            region.connect(world.get_region(connection), entrance_name)
            access_point = world.get_entrance(entrance_name)
            process_access_point(world, access_point, rulesets)


def process_access_point(world: World, access_point: Location | Entrance, rulesets):
    # preface with a false so all other rules can be combined with OR
    set_rule(access_point, lambda state: False)

    # for each ruleset in the location/entrance, call process_ruleset
    for ruleset_name, ruleset in rulesets.items():
        if ruleset_name in world.logic_sets:
            process_ruleset(world, access_point, ruleset)


def process_ruleset(world: World, access_point: Location | Entrance, ruleset: list):
    # for each access set in the ruleset, call process_access_set
    for access_set in ruleset:
        process_access_set(world, access_point, access_set)

def process_access_set(world: World, access_point: Location | Entrance, access_set: list):
    # add the rule for the access set list using oribf_has
    # this line needs to be in a separate function from the previous for loop in order to work properly 
    # (likely lambda function strangeness)
    add_rule(access_point, lambda state: all(oribf_has(world, state, item) for item in access_set), "or")
            
    
def oribf_has(world: World, state: CollectionState, item) -> bool:
    if type(item) == str:
        if item in item_dict.keys():
            # handles normal abilities like Dash, Climb, Wind, etc.
            return state.has(item, world.player)
        elif item == "Free":
            return True
        elif item == "Lure":
            return True
        elif item == "DoubleBash":
            return state.has("Bash", world.player)
        elif item == "GrenadeJump":
            return state.has_all(["Climb", "ChargeJump", "Grenade"], world.player)
        elif item == "ChargeFlameBurn":
            # requires minimum number of ability cells to get the ChargeFlameBurn ability
            return state.has("ChargeFlame", world.player) and state.has("AbilityCell", world.player, 3)
        elif item in ["ChargeDash", "RocketJump"]:
            # requires minimum number of ability cells to get the ChargeDash ability
            return state.has("Dash", world.player) and state.has("AbilityCell", world.player, 9)
        elif item == "AirDash":
            # requires minimum number of ability cells to get the AirDash ability
            return state.has("Dash", world.player) and state.has("AbilityCell", world.player, 5)
        elif item == "TripleJump":
            # requires minimum number of ability cells to get the TripleJump ability
            return state.has("DoubleJump", world.player) and state.has("AbilityCell", world.player, 16)
        elif item == "UltraDefense":
            # requires minimum number of ability cells to get the UltraDefense ability
            return state.has("AbilityCell", world.player, 19)
        elif item == "BashGrenade":
            return state.has_all(["Bash", "Grenade"], world.player)
        elif item in ["Open", "OpenWorld"]:
            # open world not implemented yet
            return False
        else:
            return False
    else:
        # if item isnt a string its a tuple (check for number of health, keystones, etc.)
        return state.has(item[0], world.player, int(item[1]))

    return False


    


def oribf_has_all(state: CollectionState, items: Set[str], player: int) -> bool:
    return all(state.has(item, player) if type(item) == str else state.has(item[0], player, int(item[1]))
               for item in items)
