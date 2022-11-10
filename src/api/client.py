import requests

headers = {
    'Authorization': 'Bearer ' + "token",
    'Content-Type': 'application/json'
}

x = requests.get("https://api.spacetraders.io/my/account", headers=headers)

print(x.text)

# https://api.spacetraders.io/game/status
# https://api.spacetraders.io/my/account
