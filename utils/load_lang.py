import json
from utils.load_environement import load_enviroment_lang

def load_main_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/main.json", "r"))

def load_loaded_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/loaded.json", "r"))

def load_template_lang():
    return json.load(open(f"lang/{load_enviroment_lang()}/template.json", "r"))