import json
from data.var import envFile

def load_enviroment():
    return json.load(open(envFile, "r"))

def load_enviroment_lang():
    try:
        return json.load(open(envFile, "r"))["LANGUAGE"].upper()
    except:
        return "EN"

def load_enviroment_token():
    return json.load(open(envFile, "r"))["TOKEN"]