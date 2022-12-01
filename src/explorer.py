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
from api import client

# api = client("TOKEN")
# api = client.from_username("example")
# token = json.loads(open("utils/example.json").read())["token"]
# api = client(token)

SYSTEMS = ("OE", "XV", "ZY1", "NA7")

USERNAME = "example"
FILE = f"utils/tokens/{USERNAME}.json"

# api = client.api.from_file(FILE)
api = client.api.from_username(USERNAME)


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

def get_systems_coordinates(*systems):
    if len(systems) == 0:
        systems = SYSTEMS
    return {s : tuple([(i["symbol"],(i["x"],i["y"])) for i in l]) for s , l in get_systems(*systems).items()}
