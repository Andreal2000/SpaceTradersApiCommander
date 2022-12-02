# TODO
# download goods if utils/goods is empty
# download systems and location if utils/systems is empty [or not equal to the server]
# generate the Travelling salesman problem solution and save on a file
# leggendo il file di prima fa viaggiare la nave per i pianeti e salva i marketplace info in utils/marketplaces
#   (combrare ad ogni pianeta la benzina se a 1 o serbatoio quasi vuoto)
# generare un grafo in base a pianeti e cosa vendono e salvarlo in utils
#
# 

import json
import math
from api import client

SYSTEMS = ("OE", "XV", "ZY1", "NA7")

TOKEN = "TOKEN"
USERNAME = "example"
FILE = f"utils/tokens/{USERNAME}.json"

# api = client.Api(TOKEN)
# api = client.Api.from_file(FILE)
api = client.Api.from_username(USERNAME)


def download_types(types):
    funct = {"goods": api.get_avaiable_goods,
             "loans": api.get_avaiable_loans,
             "ships": api.get_avaiable_ships}
    data = funct[types]()
    if dict(data).get("error") is None:
        with open(f"utils/types/{types}.json", "w") as file:
            file.write(json.dumps(data, indent=4))
    else:
        raise ValueError(data["error"]["message"])
    return data[types]

def download_goods(): return download_types("goods")
def download_loans(): return download_types("loans")
def download_ships(): return download_types("ships")


def get_types(types):
    try:
        return json.loads(open(f"utils/types/{types}.json").read())[types]
    except:
        return download_types(types)

def get_goods(): return get_types("goods")
def get_loans(): return get_types("loans")
def get_ships(): return get_types("ships")


def download_systems(*systems):
    if len(systems) == 0:
        systems = SYSTEMS
    result = {}
    for s in systems:
        data = api.get_system_locations(s)
        if dict(data).get("error") is None:
            with open(f"utils/systems/{s}.json", "w") as file:
                file.write(json.dumps(data, indent=4))
                result[s] = data["locations"]
        else:
            raise ValueError(data["error"]["message"])
    return result


def get_systems(*systems):
    if len(systems) == 0:
        systems = SYSTEMS
    result = {}
    for s in systems:
        try:
            result[s] = json.loads(open(f"utils/systems/{s}.json").read())["locations"]
        except:
            result[s] = download_systems(s)[s]
    return result


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
    return {s : [ [ h["symbol"] for h in l ] , [ [ calculate_distance(a["x"],a["y"],b["x"],b["y"]) for b in l ] for a in l ] ] for s , l in get_systems(*systems).items()}

    # {SYSTEM: [MATRIX HEADER, MATRIX], ...}
