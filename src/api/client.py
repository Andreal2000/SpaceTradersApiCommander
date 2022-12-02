import json
import requests


def generate_class(class_name, file):
    def init(self, token): self.token = token

    @classmethod
    def from_username(cls, username):
        try:
            return cls.from_file(f"utils/tokens/{username}.json")
        except:
            tmp = cls("")
            data = tmp.claim_username(username)
            del tmp
            if dict(data).get("error") is None:
                with open(f"utils/tokens/{username}.json", "w") as file:
                    file.write(json.dumps(data, indent=4))
            else:
                raise ValueError(data["error"]["message"])
            return cls(data["token"])

    @classmethod
    def from_file(cls, file):
        return cls(json.loads(open(file).read())["token"])

    with open(file) as f:
        data = json.load(f)
        endpoints = {e["method_name"]: generate_func(e) for e in data["endpoints"]}
        class_dict = dict({"__init__": init, "from_username": from_username, "from_file": from_file, "url": data["domain"], "token": ""}, **endpoints)
        return type(class_name, (), class_dict)


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
    
CLASS_NAME = "Api"
URL = "src\\api\endpoints_V1.json"

Api = generate_class(CLASS_NAME, URL)
