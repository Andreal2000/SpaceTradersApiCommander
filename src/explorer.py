# TODO
# download goods if utils/goods is empty
# download systems and location if utils/systems is empty [or not equal to the server]
# generate the Travelling salesman problem solution and save on a file
# leggendo il file di prima fa viaggiare la nave per i pianeti e salva i marketplace info in utils/marketplaces
#   (combrare ad ogni pianeta la benzina se a 1 o serbatoio quasi vuoto)
# generare un grafo in base a pianeti e cosa vendono e salvarlo in utils
#
# SYSTEMS = [OE, XV, ZY1, NA7]

import json
from api import client
# api = client("TOKEN")
# api = client.from_username("example")
# token = json.loads(open("utils/example.json").read())["token"]
# api = client(token)
FILE = "utils/tokens/example.json"
api = client.api.from_file(FILE)
print(api.get_system_locations("OE"))


def download_types(type):
    types = {"goods": api.get_avaiable_goods,
             "loans": api.get_avaiable_loans,
             "ships": api.get_avaiable_ships}
    data = types[type]()
    if dict(data).get("error") is None:
        with open(f"utils/types/{type}.json", "x") as file:
            file.write(json.dumps(data, indent=4))
    else:
        raise ValueError(data["error"]["message"])
    return data[type]


def download_goods():
    return download_types("goods")


def get_goods():
    # if file exist read else download
    return


def download_loans():
    return download_types("loans")


def download_ships():
    return download_types("ships")


def download_systems():
    print()
