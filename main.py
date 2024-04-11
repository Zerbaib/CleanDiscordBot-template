import json
import os
import platform

import aiohttp
import disnake
from disnake.ext import commands

from utils.load_environement import load_enviroment_lang, load_enviroment_token
from utils.load_lang import load_main_lang
from data.var import *

lang = load_main_lang()

for files in dataFilePath.values():
    if not os.path.exists(files):
        with open(files, 'w') as file:
            json.dump({}, file)

if not os.path.exists(envFilePath):
    token = input(lang.get("QUESTION_BOT_TOKEN"))
    lang_choice = input(lang.get("QUESTION_LANGUAGE"))
    lang_possible = ["en", "fr", "EN", "FR"]
    if lang_choice in lang_possible:
        lang_choice = lang_choice.upper()
    else:
        print(lang.get("ERROR_INVALID_LANGUAGE"))
        lang_choice = "EN"
    with open(envFilePath, 'w') as env_file:
        envData = {
            "LANGUAGE": lang_choice,
            "TOKEN": token
        }
        json.dump(envData, env_file, indent=4)

if not os.path.exists(badWordFilePath):
    badword_data = {
        "bad_words": [
            "badword1",
            "badword2",
            "badword3"
        ]
    }
    with open(badWordFilePath, 'w') as badword_file:
        json.dump(badword_data, badword_file, indent=4)

if not os.path.exists(configFilePath):
    with open(configFilePath, 'w') as config_file:
        prefix = input(lang.get("QUESTION_PREFIX"))
        logID = int(input(lang.get("QUESTION_LOG_CHANNEL_ID")))
        pollID = int(input(lang.get("QUESTION_POLL_CHANNEL_ID")))
        joinID = int(input(lang.get("QUESTION_WELCOME_CHANNEL_ID")))
        leaveID = int(input(lang.get("QUESTION_LEAVE_CHANNEL_ID")))
        voiceID = int(input(lang.get("QUESTION_VOICE_CHANNEL_ID")))
        ownerID = int(input(lang.get("QUESTION_OWNER_ID")))
        muteID = int(input(lang.get("QUESTION_MUTE_ROLE_ID")))
        rank1 = int(input(lang.get("QUESTION_XP_ROLE_10_ID")))
        rank2 = int(input(lang.get("QUESTION_XP_ROLE_25_ID")))
        rank3 = int(input(lang.get("QUESTION_XP_ROLE_50_ID")))
        config_data = {
            "PREFIX": prefix,
            "LOG_ID": logID,
            "POLL_ID": pollID,
            "JOIN_ID": joinID,
            "LEAVE_ID": leaveID,
            "AUTO_VOICE_ID": voiceID,
            "YOUR_ID": ownerID,
            "MUTE_ROLE_ID": muteID,
            "del_time": 3,
            "level_roles": {
                "10": rank1,
                "25": rank2,
                "50": rank3
            }
        }
        json.dump(config_data, config_file, indent=4)

try:
    with open(configFilePath, 'r') as config_file:
        config = json.load(config_file)
except Exception as e:
    print(lang.get("ERROR_CONFIG_FILE").format(e))
    exit()

prefix = config["PREFIX"]
botLang = load_enviroment_lang()

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True
)
bot.remove_command('help')

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        botName = bot.user.name
    else:
        botName = bot.user.name + "#" + bot.user.discriminator

    async with aiohttp.ClientSession() as session:
        async with session.get(onlineVersion) as response:
            if response.status == 200:
                botRepoVersion = await response.text()
            else:
                botRepoVersion = "Unknown"

    with open(localVersionFilePath, 'r') as version_file:
        botVersion = version_file.read().strip()

    if botVersion != botRepoVersion:
        print()
        print('===============================================')
        print('🛑 You are not using the latest version!')
        print('🛑 Please update the bot.')
        print('🛑 Use "git fetch && git pull" to update your bot.')
    print('===============================================')
    print(f"🔱 The bot is ready!")
    print(f'🔱 Logged in as {botName} | {bot.user.id}')
    print(f'🔱 Language: {botLang}')
    print(f'🔱 Bot local version: {botVersion}')
    print(f'🔱 Bot online version: {botRepoVersion}')
    print(f"🔱 Disnake version: {disnake.__version__}")
    print(f"🔱 Running on {platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Python version: {platform.python_version()}")
    print('===============================================')

for files in utilsCogPath.values():
    try:
        bot.load_extension(files)
    except Exception as e:
        print(lang.get("ERROR_COG_LOADING").format(cogName=files, e=e))

for element in os.listdir(cogsFolder):
    try:
        element_dir = f"{cogsFolder}{element}"
        if os.path.isdir(element_dir):
            for filename in os.listdir(element_dir):
                if filename.endswith('.py'):
                    cog_name = filename[:-3]
                    try:
                        bot.load_extension(f'cogs.plugins.{element}.{cog_name}')
                    except Exception as e:
                        print(lang.get("ERROR_COG_LOADING").format(cogName=cog_name, e=e))
    except Exception as e:
        print(lang.get("ERROR_ELEMENTS_LOADING").format(element, e))


bot.run(load_enviroment_token())