from typing import Set, cast

from .RulesData import location_rules
from .RulesData import connection_rules
from .Items import item_dict
from .Locations import OriBlindForestLocation
from .Options import OriBlindForestOptions
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


def process_access_point(world: World, access_point: Location | Entrance, rulesets: dict[str, list[list[str | tuple[str, int]]]]):
    # preface with a false so all other rules can be combined with OR
    set_rule(access_point, lambda state: False)

    # for each ruleset in the location/entrance, call process_ruleset
    for ruleset_name, ruleset in rulesets.items():
        if ruleset_name in world.logic_sets:
            process_ruleset(world, access_point, ruleset)


def process_ruleset(world: World, access_point: Location | Entrance, ruleset: list[list[str | tuple[str, int]]]):
    # for each access set in the ruleset, call process_access_set
    for access_set in ruleset:
        process_access_set(world, access_point, access_set)

def process_access_set(world: World, access_point: Location | Entrance, access_set: list[str | tuple[str, int]]):
    # add the rule for the access set list using oribf_has
    # this line needs to be in a separate function from the previous for loop in order to work properly 
    # (likely lambda function strangeness)
    add_rule(access_point, lambda state: all(oribf_has(world, state, item) for item in access_set), "or")
            
    
def oribf_has(world: World, state: CollectionState, item: str | tuple[str, int]) -> bool:
    options: OriBlindForestOptions = cast(OriBlindForestOptions, world.options)

    if type(item) == str:
        if item in item_dict.keys():
            # handles normal abilities like Dash, Climb, Wind, etc.
            return state.has(item, world.player)
        
        elif item == "Free":
            return True
        
        elif item == "Lure":
            return options.enable_lure == True
        
        elif item == "DoubleBash":
            return options.enable_double_bash == True and state.has("Bash", world.player)
        
        elif item == "GrenadeJump":
            return options.enable_grenade_jump == True and state.has_all(["Climb", "ChargeJump", "Grenade"], world.player)
        
        elif item == "ChargeFlameBurn":
            return options.enable_charge_flame_burn == True and \
                state.has("ChargeFlame", world.player) and state.has("AbilityCell", world.player, 3)
        
        elif item in ["ChargeDash", "RocketJump"]:
            return options.enable_charge_dash == True and \
                state.has("Dash", world.player) and state.has("AbilityCell", world.player, 6)
        
        elif item == "AirDash": 
            return options.enable_air_dash == True and \
                state.has("Dash", world.player) and state.has("AbilityCell", world.player, 3)
        
        elif item == "TripleJump":
            return options.enable_triple_jump == True and \
                state.has("DoubleJump", world.player) and state.has("AbilityCell", world.player, 12)
        
        elif item == "UltraDefense":
            return options.enable_damage_boost == True and state.has("AbilityCell", world.player, 12)
        
        elif item == "BashGrenade":
            return state.has_all(["Bash", "Grenade"], world.player)
        
        elif item in ["Open", "OpenWorld"]:
            # open world not implemented yet
            return False
        else:
            return False
    else:
        # if item isnt a string its a tuple (check for number of health, keystones, etc.)
        # if item is a health cell, only add it if damage boost is enabled
        if (item[0] == "HealthCell" and options.enable_damage_boost == True) or item[0] != "HealthCell":
            return state.has(item[0], world.player, int(item[1]))

    return False


    


def oribf_has_all(state: CollectionState, items: Set[str], player: int) -> bool:
    return all(state.has(item, player) if type(item) == str else state.has(item[0], player, int(item[1]))
               for item in items)
