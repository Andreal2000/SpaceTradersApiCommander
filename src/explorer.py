import time
from downloader import *
from itertools import permutations
import math


def calculate_distance(x1, y1, x2, y2):
    return round(math.sqrt((x2-x1)**2 + (y2-y1)**2))


def calculate_time(distance, speed):
    SYSTEM_SCALE = 3
    DOCKING_SECONDS = 30
    return ((distance * SYSTEM_SCALE) / speed) + DOCKING_SECONDS


def calculate_fuel_cost(distance, fuel_efficiency, docking_efficiency, origin_location_type):
    flight_cost = math.round((distance * fuel_efficiency) / 30)
    docking_cost = (docking_efficiency if origin_location_type == "PLANET" else 0) + 1
    return flight_cost + docking_cost


def get_systems_matrix(*systems):
    if len(systems) == 0:
        systems = SYSTEMS
    return {s: [[h["symbol"] for h in l], [[calculate_distance(a["x"], a["y"], b["x"], b["y"]) for b in l] for a in l]] for s, l in get_systems(*systems).items()}


def travelling_salesman_problem(*systems):
    if len(systems) == 0:
        systems = SYSTEMS

    def inner(system):
        header = system[0]
        system = system[1]
        m = min([(sum([system[p[i]][p[(i+1) % len(p)]] for i in range(len(p))]), p) for p in permutations(range(len(system))) if p < p[::-1]])
        return [header[i] for i in m[1]]

    def inner_apx(system):
        header = system[0]
        system = system[1]
        out = []
        rm = []
        nh = {}

        for h in header:
            if len(h.split("-")) == 3 and h.split("-")[1] != "W":
                p = "-".join(h.split("-")[:2])
                if nh.get(p) is None:
                    nh[p] = [h]
                else:
                    nh[p] = nh[p] + [h]
                    rm += [header.index(h)]
            else:
                nh[h] = []

        for x in reversed(range(len(system))):
            if x in rm:
                del system[x]
            else:
                for y in reversed(rm):
                    del system[x][y]
        
        m = min([(sum([system[p[i]][p[(i+1) % len(p)]] for i in range(len(p))]), p) for p in permutations(range(len(system))) if p < p[::-1]])
        # m = (569, (0, 1, 7, 10, 4, 5, 8, 6, 9, 3, 2)) # ZY1

        k = list(nh.keys())
        for i in m[1]:
            out.append(k[i])
            if nh.get(k[i]) is not None and len(nh.get(k[i])) > 0:
                out.extend(nh[k[i]])
        return out

    for k, v in get_systems_matrix(*systems).items():
        with open(f"utils/systems/tsp/TSP_{k}.json", "w") as file:
            file.write(json.dumps({k: inner(v) if len(v[1]) <= 11 else inner_apx(v)}, indent=4))


def get_system_TSP(system):
    if len(system) == 0 or system == None:
        raise Exception
    return json.loads(open(f"utils/systems/tsp/TSP_{system}.json").read())[system]

# TODO REMOVE API FROM DECLARETION WHEN MOVE ALL INTO A CLASS
def fill_ship(api, ship):
    ship = api.get_ship_info(ship["id"])["ship"]
    while ship['spaceAvailable'] != 0:
        res = api.new_purchase(ship['id'], 'FUEL', min(ship['spaceAvailable'], ship['loadingSpeed']))
        ship = res["ship"]
    return ship

def explore_systems():
    # Get fastest ship
    ships = api.get_ships()
    if len(ships['ships']) == 0: 
        raise Exception
    elif len(ships['ships']) == 1:
        ship = ships['ships'][0]
    else:
        ship = sorted(ships['ships'], key=lambda s: s["speed"], reverse=True)[0]

    # Get symbols of the current marketplace
    symbols = api.get_marketplace(ship['location'])['marketplace']
    symbols = [m['symbol'] for m in symbols]

    # Sell or jettison all excepts FUEL
    for good in ship['cargo']:
        if good['good'] != 'FUEL':
            if good['good'] in symbols:
                api.new_sell(ship['id'], good['good'], good['quantity'])
            else:
                api.jettison_cargo(ship['id'], good['good'], good['quantity'])

    # Buy FUEL (spaceAvailable is max_cargo - `current FUEL`)
    ship = fill_ship(api, ship)

    system_TSP = get_system_TSP(ship['location'].split('-')[0])
    system_TSP = (system_TSP[system_TSP.index(ship["location"])+1:] +
                  system_TSP[:system_TSP.index(ship["location"])+1])

    for s in system_TSP:
        fp = api.new_flight_plan(ship["id"], s)["flightPlan"]
        time.sleep(fp["timeRemainingInSeconds"] + 1)
        marketplace = api.get_marketplace(s)
        with open(f"utils/marketplaces/{s.split('-')[0]}/{s}.json", "w") as file:
            file.write(json.dumps(marketplace, indent=4))
        ship = fill_ship(api, ship)

def get_materials_seller(system, symbol):
    marketpalces = get_marketpalces(system)[system]
    res = []

    for location, materials in marketpalces.items():
        for material in materials:
            if material["symbol"] == symbol:
                res.append(location)
    
    return res

def generate_graphs(*systems):
	# For each system
    # { A : 
    #       {
    #        <type> : [B, C, D] ,
	#		 <...> : [...] ,
    #       }
	# },
	# { B :
	#		...
	# },

    if len(systems) == 0:
        systems = SYSTEMS

    system_location_materials = {}
    marketpalces = get_marketpalces(*systems)

    for system, locations in marketpalces.items():
        system_location_materials[system] = {}
        for location, materials in locations.items():
            system_location_materials[system][location] = {} 
            for material in materials:
                system_location_materials[system][location][material["symbol"]] = get_materials_seller(system, material["symbol"])

    for s in systems:
        with open(f"utils/graphs/{s}.json", "w") as file:
            file.write(json.dumps(system_location_materials[s], indent=4))
