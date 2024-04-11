import json
import os
import platform

import aiohttp
import disnake
from disnake.ext import commands

from utils.load_environement import load_enviroment_lang, load_enviroment_token
from utils.load_lang import load_main_lang
from data.var import *

lang = load_enviroment_lang()

if not os.path.exists(envFilePath):
    token = input(lang("QUESTION_BOT_TOKEN"))
    lang_choice = input(lang("QUESTION_LANGUAGE"))
    lang_possible = ["en", "fr", "EN", "FR"]
    if lang_choice in lang_possible:
        lang_choice = lang_choice.upper()
    else:
        print("Invalid language, default language is English")
        lang_choice = "EN"
    with open(envFilePath, 'w') as env_file:
        envData = {
            "LANGUAGE": lang_choice,
            "TOKEN": token
        }
        json.dump(envData, env_file, indent=4)

for files in dataFilePath.values():
    if not os.path.exists(files):
        with open(files, 'w') as file:
            json.dump({}, file)

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
        prefix = input("Enter the bot's prefix:\n")
        log_id = int(input("Enter the log's channel ID:\n"))
        poll_id = int(input("Enter the poll's channel ID:\n"))
        join_id = int(input("Enter the join's channel ID:\n"))
        leave_id = int(input("Enter the leave's channel ID:\n"))
        voice_id = int(input("Enter the voice's channel ID\nUsed for create salon on join:\n"))
        id_client = int(input("Enter your Discord ID:\n"))
        mute_id = int(input("Enter role id of muted role:\n"))
        rank1 = int(input("Enter role id of level 10 role:\n"))
        rank2 = int(input("Enter role id of level 25 role:\n"))
        rank3 = int(input("Enter role id of level 50 role:\n"))
        config_data = {
            "PREFIX": prefix,
            "LOG_ID": log_id,
            "POLL_ID": poll_id,
            "JOIN_ID": join_id,
            "LEAVE_ID": leave_id,
            "AUTO_VOICE_ID": voice_id,
            "YOUR_ID": id_client,
            "MUTE_ROLE_ID": mute_id,
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
    print(f"🌪️  Error during config loading:\n\n{e}")
    exit()

prefix = config["PREFIX"]
ln = load_enviroment_lang()

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True
)
bot.remove_command('help')

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        nbot = bot.user.name
    else:
        nbot = bot.user.name + "#" + bot.user.discriminator

    async with aiohttp.ClientSession() as session:
        async with session.get(onlineVersion) as response:
            if response.status == 200:
                bot_repo_version = await response.text()
            else:
                bot_repo_version = "Unknown"

    with open(localVersionFilePath, 'r') as version_file:
        bot_version = version_file.read().strip()

    if bot_version != bot_repo_version:
        print()
        print('===============================================')
        print('🛑 You are not using the latest version!')
        print('🛑 Please update the bot.')
        print('🛑 Use "git fetch && git pull" to update your bot.')
    print('===============================================')
    print(f"🔱 The bot is ready!")
    print(f'🔱 Logged in as {nbot} | {bot.user.id}')
    print(f'🔱 Language: {ln}')
    print(f'🔱 Bot local version: {bot_version}')
    print(f'🔱 Bot online version: {bot_repo_version}')
    print(f"🔱 Disnake version: {disnake.__version__}")
    print(f"🔱 Running on {platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Python version: {platform.python_version()}")
    print('===============================================')

for files in utilsCogPath.values():
    try:
        bot.load_extension(files)
    except Exception as e:
        print(f"🌪️  Error during '{files}' loading:\n\n{e}")

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
                        print(f"🌪️  Error during '{cog_name}' loading:\n\n{e}")
    except Exception as e:
        print(f"🌪️  Error during '{element}' loading:\n\n{e}")


bot.run(load_enviroment_token())