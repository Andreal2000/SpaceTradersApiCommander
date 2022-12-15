import json
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
