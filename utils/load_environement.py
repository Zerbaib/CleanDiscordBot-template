import json
from data.var import envFilePath

def load_enviroment():
    return json.load(open(envFilePath, "r"))

def load_enviroment_lang():
    try:
        return json.load(open(envFilePath, "r"))["LANGUAGE"].upper()
    except:
        return "EN"

def load_enviroment_token():
    return json.load(open(envFilePath, "r"))["TOKEN"]