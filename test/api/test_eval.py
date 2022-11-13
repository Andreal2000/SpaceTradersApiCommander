import json
import requests

test = {
    "http_method": "GET",
    "endpoint": "my/account/",  # "my/account/{shipId}"
    "url_params": [],
    "body_params": [],
    "method_name": "getAccountInfo",
    "method_docs": "Get information on your account",
}

URL = "https://api.spacetraders.io/"

# def readjson(file):
#     generate_func(data)


def generate_func(data):
    template = """lambda self {method_params}: requests.{http_method}(
        url=self.url + f"{endpoint}", 
        headers={{'Authorization': 'Bearer ' + self.token,'Content-Type': 'application/json'}},
        params={body_params})"""

    method_params_list = data["url_params"]+data["body_params"]
    method_params = "" if method_params_list is [] else "".join(
        [f", {x}" for x in method_params_list])
    body_params = "None" if data["body_params"] == [
    ] else "{" + ", ".join([f"'{x}': {x}" for x in data["body_params"]]) + "}"

    func = template.format(
        method_params=method_params,
        http_method=data["http_method"].lower(),
        endpoint=data["endpoint"],
        body_params=body_params)

    return eval(func)


myclass = type("myclass", (), {"url": "https://api.spacetraders.io/",
               "token": "", test["method_name"]: generate_func(test)})

m = myclass()
print(m.getAccountInfo().text)
