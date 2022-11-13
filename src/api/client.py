import requests
import json

URL = "https://api.spacetraders.io/"

token = ""

test = {"methodName": "getAccountInfo",
        "methodArgs": None,
        "methodDocs": "Get information on your account",
        "HTTPmethod": "GET",
        "endpoint": "my/account",
        "params": None}

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}

# ??? dynamic method args = eval()

# params = None if params is None else json.dumps(params)
# requests.get(url, headers=headers, params=params)
x = requests.get("https://api.spacetraders.io/my/account", headers=headers)

# myclass = type("myclass",(object),{"methodName":"method"})

print(x.text)


# lambda self,  urlArgs + params : {}

# def createfun(test):{
#     s = s.format(test)
#     return eval(string)
# }

""" lambda self, {test["methodArgs"]}: 

    requests.{test["HTTPmethod"]}(
        url= self.URL + {test["endpoint"]}, 
        headers={
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
            },
        params={test["params"]})
  """

# https://api.spacetraders.io/

# https://api.spacetraders.io/users/:username/claim POST Claim a username and get a token
#
# https://api.spacetraders.io/game/status GET Use to determine whether the server is alive
#
# https://api.spacetraders.io/game/leaderboard/net-worth GET Use to see the current net worth of the top players
#
# https://api.spacetraders.io/my/account GET Get information on your account
#
# FLIGHT PLANS
#
# https://api.spacetraders.io/my/flight-plans/:flightPlanId GET Get info on an existing flight plan
#
# https://api.spacetraders.io/my/flight-plans POST Submit a new flight plan (shipId & destination)
#
# LOANS
#
# https://api.spacetraders.io/my/loans GET Get your loans
#
# https://api.spacetraders.io/my/loans/:loanId PUT Pay off your loan
#
# https://api.spacetraders.io/my/loans POST Take out a loan (type)
#
# PURCHASE/SELL
#
# https://api.spacetraders.io/my/purchase-orders POST Place a new purchase order (shipId & good & quantity)
#
# https://api.spacetraders.io/my/sell-orders POST Place a new sell order (shipId & good & quantity) 

# SHIPS
#
# https://api.spacetraders.io/my/ships POST Buy a new ship (location & type)
#
# https://api.spacetraders.io/my/ships/:shipId GET Get your ship info
#
# https://api.spacetraders.io/my/ships GET Get your ships
#
# https://api.spacetraders.io/my/ships/:shipId/jettison POST Jettison cargo (good & quantity)
#
# https://api.spacetraders.io/my/ships/:shipId/ DELETE Scrap your ship for credits
#
# https://api.spacetraders.io/my/ships/:fromShipId/transfer POST Transfer cargo between ships (toShipId & good & quantity)
#
# https://api.spacetraders.io/my/warp-jumps POST Attempt a warp jump
#
# LOCATIONS
#
# https://api.spacetraders.io/locations/:locationSymbol GET Get info on a location
#
# https://api.spacetraders.io/locations/:locationSymbol/marketplace GET Get info on a location's marketplace
#
# https://api.spacetraders.io/locations/:locationSymbol/ships GET Get the ships at a location
#
# SYSTEMS
#
# https://api.spacetraders.io/systems/:systemSymbol/ship-listings GET Get a list of all available ships in the system.
#
# https://api.spacetraders.io/systems/:systemSymbol/flight-plans GET Get all active flight plans in the system.
#
# https://api.spacetraders.io/systems/:systemSymbol/ships GET Get info on a system's docked ships
#
# https://api.spacetraders.io/systems/:systemSymbol/locations GET Get location info for a system
#
# https://api.spacetraders.io/systems/:systemSymbol GET Get systems info
#
# TYPES
#
# https://api.spacetraders.io/types/goods GET Get available goods
#
# https://api.spacetraders.io/types/loans GET Get available loans
#
# https://api.spacetraders.io/types/ships GET Get info on available ships
#
# STRUCTURES WIP
#
# https://api.spacetraders.io/game/status
# https://api.spacetraders.io/my/account
