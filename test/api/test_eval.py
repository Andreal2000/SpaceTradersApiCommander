import json
import requests


def generate_class(file):
    def init(self, token): self.token = token

    @classmethod
    def from_username(cls, username):
        tmp = cls("")
        data = tmp.claim_username(username)
        del tmp
        if dict(data).get("error") == None:
            with open(f"utils/tokens/{username}.json", "x") as file:
                file.write(json.dumps(data))
        else:
            raise ValueError(data["error"]["message"])
        return cls(data["token"])

    with open(file) as f:
        data = json.load(f)
        endpoints = {e["method_name"]: generate_func(e) for e in data["endpoints"]}
        class_dict = dict({"__init__": init, "from_username": from_username, "url": data["domain"], "token": ""}, **endpoints)
        return type("client", (), class_dict)


def generate_func(data):
    template = """lambda self {method_params}: requests.{http_method}(
        url=self.url + f"{endpoint}", 
        headers={{'Authorization': 'Bearer ' + self.token,'Content-Type': 'application/json'}},
        params={body_params}).json()"""

    method_params_list = data["url_params"]+data["body_params"]
    method_params = "" if method_params_list is [] else "".join([f", {x}" for x in method_params_list])
    body_params = "None" if data["body_params"] == [] else "{" + ", ".join([f"'{x}': {x}" for x in data["body_params"]]) + "}"

    str_func = template.format(
        method_params=method_params,
        http_method=data["http_method"].lower(),
        endpoint=data["endpoint"],
        body_params=body_params)

    func = eval(str_func)
    func.__doc__ = data["method_docs"]
    return func

myclass = generate_class("src\\api\endpoints_V1.json")
m = myclass("TOKEN")
# m = myclass.from_username("example")
# token = json.loads(open("utils/examplre.json").read())["token"]
# m = myclass(token)
print(m.get_account_info())
