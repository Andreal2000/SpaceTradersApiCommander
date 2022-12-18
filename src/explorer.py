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


def tmp():
    # Get fastest ship
    ships = api.get_ships()
    if len(ships['ships']) == 0: 
        raise Exception
    elif len(ships['ships']) == 1:
        ship = ships['ships'][0]
    else:
        ship = sorted(ships['ships'], key=lambda s: s["speed"], reverse=True)[0]
    # print(ship)

    # Get symbols of the current marketplace
    marketplace = api.get_marketplace(ship['location'])['marketplace']
    symbols = [m['symbol'] for m in marketplace]
    # print(symbols)

    # Sell or jettison all excepts FUEL
    for good in ship['cargo']:
        if good['good'] != 'FUEL':
            if good['good'] in symbols:
                api.new_sell(ship['id'], good['good'], good['quantity'])
            else:
                api.jettison_cargo(ship['id'], good['good'], good['quantity'])

    # Buy FUEL (spaceAvailable is max_cargo - `current FUEL`)
    ship = api.get_ship_info(ship["id"])["ship"]
    while ship['spaceAvailable'] != 0:
        res = api.new_purchase(ship['id'], 'FUEL', min(ship['spaceAvailable'], ship['loadingSpeed']))
        ship = res["ship"]

    # system_TSP = get_system_TSP(ship['location'].split('-')[0])
    # print(system_TSP)

    # do TSP
    # for each planet get marketplace

tmp()

# TODO
# leggendo il file di prima fa viaggiare la nave per i pianeti e salva i marketplace info in utils/marketplaces
#   (combrare ad ogni pianeta la benzina se a 1 o serbatoio quasi vuoto)
# generare un grafo in base a pianeti e cosa vendono e salvarlo in utils
