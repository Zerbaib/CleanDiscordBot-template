import json
from utils.load_environement import load_enviroment_lang

def load_main_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/main.json", "r"))