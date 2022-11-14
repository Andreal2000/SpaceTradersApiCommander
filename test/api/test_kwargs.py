import json
import requests

test = {
    "http_method": "GET",
    "endpoint": "my/account/",
    "url_params": None,
    "body_params": None,
    "method_name": "getAccountInfo",
    "method_docs": "Get information on your account",
}

def generate_func(data):
    http_method, endpoint = list(data.values())[:2]
    method = {"GET": requests.get,
              "POST": requests.post,
              "PUT": requests.put,
              "DELETE": requests.delete, }

    a,b= object("a"),("b")
    x = lambda self, **kwargs: method[http_method](
        url=self.url + endpoint.format(kwargs["url_params"] if "url_params" in kwargs.keys() else ""),
        headers={
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'},
        params=None if "body_params" not in kwargs.keys() is None else json.dumps(
            kwargs["body_params"] if "body_params" in kwargs.keys() else "")
    )
    # x = lambda self, **kwargs: method[http_method](
    #     url=self.url + endpoint.format(kwargs["url_params"] if "url_params" in kwargs.keys() else ""),
    #     headers={
    #         'Authorization': 'Bearer ' + self.token,
    #         'Content-Type': 'application/json'},
    #     params=None if "body_params" not in kwargs.keys() is None else json.dumps(
    #         kwargs["body_params"] if "body_params" in kwargs.keys() else "")
    # )

    return x


print(generate_func(test))


# class a():
#     def __init__(self):
#         self.url = "https://api.spacetraders.io/"
#         self.token = ""
#         self.ciao = ""


# b = a()

# b.ciao = generate_func(test)

# print(b.ciao(b, url_params=None, body_params=None).text)

myclass = type("myclass", (), {"url": "https://api.spacetraders.io/",
               "token": "", test["method_name"]: generate_func(test)})

m = myclass()
m.getAccountInfo()
