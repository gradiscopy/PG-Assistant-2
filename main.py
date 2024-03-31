import os
from colorama import Fore
import time
from modules.console import Logger

print(Fore.YELLOW + "| [INFO] Checking for modules...")
time.sleep(5)
os.system('cls' if os.name == 'nt' else 'clear')


def check_modules(required_modules):
    for module in required_modules:
        try:
            __import__(module)
            Logger.error(Fore.RED + f" {module} is already installed.")
        except ImportError:
            return False
    return True

def install_modules():
    required_modules = ['aiohttp', 'colorama', 'requests', 'asyncio', 'datetime']

    if check_modules(required_modules):
        Logger.error(Fore.RED + " You already installed all modules!")
        return

    Logger.info(Fore.YELLOW + "Installing modules...")
    for module in required_modules:
        os.system(f'pip install {module}')
        Logger.info(Fore.GREEN + f" Installed module: {module}")

install_modules()

import aiohttp, asyncio, json, random, requests
from datetime import datetime
import threading

with open("config.json", "r") as f:
    config = json.load(f)

webhook = config.get("webhook_url")
min_id = config.get("min_userid_to_snipe")
max_id = config.get("max_userid_to_snipe")    

version = "v1.2.0"

os.system('cls' if os.name == 'nt' else 'clear')
Logger.info(Fore.YELLOW + " Checking version...")
time.sleep(5)
Logger.info(Fore.YELLOW + " Checking webhook...")
time.sleep(2.9)
Logger.info(Fore.YELLOW + " Starting bot...")
time.sleep(5)
os.system('cls' if os.name == 'nt' else 'clear')

print(Fore.CYAN + """
 __  ___  _______  __       __      ____    ____    .______     _______ 
|  |/  / |   ____||  |     |  |     \   \  /   /    |   _  \   /  _____|
|  '  /  |  |__   |  |     |  |      \   \/   /     |  |_)  | |  |  __  
|    <   |   __|  |  |     |  |       \_    _/      |   ___/  |  | |_ | 
|  .  \  |  |____ |  `----.|  `----.    |  |        |  |      |  |__| | 
|__|\__\ |_______||_______||_______|    |__|        | _|       \______|
""")
print(Fore.LIGHTWHITE_EX + "────────────────────────────────")
print(Fore.LIGHTCYAN_EX + "| >> This is searcher old accs for PG")
print(Fore.LIGHTWHITE_EX + "────────────────────────────────")
print(Fore.LIGHTCYAN_EX + "| >> What is PG?")
print(Fore.LIGHTCYAN_EX + "| > PG: Password guesser")
print(Fore.LIGHTWHITE_EX + "────────────────────────────────")
print(Fore.LIGHTCYAN_EX + "| >> Main")
print(Fore.LIGHTCYAN_EX + f"| > Max ID: {max_id}")
print(Fore.LIGHTCYAN_EX + f"| > Min ID: {min_id}")
print(Fore.LIGHTCYAN_EX + f"| > Webhook to send: {webhook}")
print(Fore.LIGHTWHITE_EX + "────────────────────────────────")
print(Fore.LIGHTCYAN_EX + "| >> Credits")
print(Fore.LIGHTCYAN_EX + "| > Original version of this bot: https://github.com/zkoolol/Roblox-PG-Assistant")
print(Fore.LIGHTCYAN_EX + "| > Made by kellyhated, zkoolol (github)")
print(Fore.LIGHTCYAN_EX + "| > Discord server with updates: .gg/73y53QZfjA")
print(Fore.LIGHTWHITE_EX + "────────────────────────────────")
print(Fore.LIGHTCYAN_EX + "| >> Misc")
print(Fore.LIGHTCYAN_EX + "| > Vouch here if u got acc: .gg/73y53QZfjA")
print(Fore.LIGHTCYAN_EX + f"| > Version: {version}")
print(Fore.LIGHTWHITE_EX + "────────────────────────────────")

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def username(session, user_id):
    while True:
        response = await fetch(session, f"https://users.roblox.com/v1/users/{user_id}")
        if "name" in response:
            return response["name"]
        elif "status" in response and response["status"] == 429:
            await asyncio.sleep(1)
            Logger.error(Fore.YELLOW + f" Ratelimited | User ID: {user_id}")
        else:
            Logger.error(Fore.RED + f" Username not found | User ID: {user_id}")
            return None

async def created(session, user_id):
    while True:
        response = await fetch(session, f"https://users.roblox.com/v1/users/{user_id}")
        if "created" in response:
            created_date = response["created"]
            datetime_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"]
            for format_str in datetime_formats:
                try:
                    created_year = datetime.strptime(created_date, format_str).year
                    return created_year
                except ValueError:
                    continue
            Logger.error(Fore.RED + f" Unable to get creation date | User ID: {user_id}")
            return None
        elif "status" in response and response["status"] == 429:
            await asyncio.sleep(1)
            Logger.error(Fore.YELLOW + f" Ratelimited | User ID: {user_id}")
        else:
            Logger.error(Fore.RED + f" Unable to get creation date | User ID: {user_id}")
            return None

async def avatar_thumbnail(session, user_id):
    response = await fetch(session, f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=250x250&format=Png&isCircular=true")
    return response["data"][0]["imageUrl"] if "data" in response else None

async def verified(session, user_id, asset_ids):
    verified_assets = []
    for asset_id in asset_ids:
        while True:
            response = await fetch(session, f"https://inventory.roblox.com/v1/users/{user_id}/items/Asset/{asset_id}")
            if "data" in response and response["data"]:
                verified_assets.append(asset_id)
                break
            elif "status" in response and response["status"] == 429:
                await asyncio.sleep(1)
                Logger.warning(Fore.YELLOW + f" Ratelimited | User ID: {user_id}")
            else:
                break
    return verified_assets if verified_assets else None

async def last_online(session, user_id):
    payload = {"userIds": [user_id]}
    while True:
        response = await session.post("https://presence.roblox.com/v1/presence/last-online", json=payload)
        response_data = await response.json()
        if "lastOnlineTimestamps" in response_data:
            last_online_timestamps = response_data["lastOnlineTimestamps"]
            if last_online_timestamps:
                last_online = last_online_timestamps[0].get("lastOnline")
                if last_online:
                    datetime_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"]
                    for format_str in datetime_formats:
                        try:
                            last_online_datetime = datetime.strptime(last_online, format_str)
                            return last_online_datetime
                        except ValueError:
                            continue
            Logger.error(Fore.RED + f" Unable to get last online date | User ID: {user_id}")
            return None
        elif "status" in response_data and response_data["status"] == 429:
            await asyncio.sleep(1)
            Logger.error(Fore.YELLOW + f" Ratelimited | User ID: {user_id}")
        else:
            Logger.error(Fore.RED + f" Unable to get last online date | User ID: {user_id}")
            return None

async def rap(session, user_id, cursor, rap=0):
    response = await fetch(session, f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=100&cursor={cursor}")
    if "data" in response:
        for i in response["data"]:
            if "recentAveragePrice" in i and i["recentAveragePrice"] is not None:
                rap += i["recentAveragePrice"]
    if "nextPageCursor" in response and response["nextPageCursor"] is not None:
        return await rap(session, user_id, response["nextPageCursor"], rap)
    return rap

total_scraped = 0

async def main(webhook_url, min_id, max_id):
    async with aiohttp.ClientSession() as session:
        user_id = random.randint(min_id, max_id)

        asset_ids_to_check = [18824203, 1567446, 93078560, 102611803]
        verified_assets = []

        for asset_id in asset_ids_to_check:
            assets = await verified(session, user_id, [asset_id])
            if assets:
                verified_assets.extend(assets)

        user_rap = await rap(session, user_id, "", 0)
        roblox_username = await username(session, user_id)
        created_year = await created(session, user_id)
        last_online_date = await last_online(session, user_id)
        verified_status = bool(verified_assets)

        user_info = requests.get(url=f"https://users.roblox.com/v1/users/{user_id}").json()
        description = user_info["description"].replace("\n", " ")
        isbanned = user_info ["isBanned"]

        if description is None:
            description = "None"        

        if created_year is None:
            Logger.error(Fore.RED + f" Unable to get creation date | User ID: {user_id}")
            return

        if last_online_date is None:
            Logger.error(Fore.RED + f" Unable to get last online date | User ID: {user_id}")
            return

        offline_years = config.get("offline_years")

        if last_online_date.year > datetime.now().year - offline_years:
            None
            return

        created_year_str = str(created_year)
        last_online_date_str = last_online_date.strftime("%B %d, %Y")
        
        global total_scraped 

        embed = {
            "title": f":bell: Scraped new user for PG ({roblox_username})",
            "description": f":gem: Total users scraped: {total_scraped}",
            "color": 5763719,
            "url": f"https://roblox.com/users/{user_id}",
            "thumbnail": {"url": await avatar_thumbnail(session, user_id)},
            "fields": [
                {"name": ":coral: User ID:", "value": user_id, "inline": True},
                {"name": ":bust_in_silhouette: Username:", "value": roblox_username, "inline": True},
                {"name": ":newspaper: Description:", "value": f"```{description}```" if description else "User doesnt have description.", "inline": True},                
                {"name": ":baby: Created Year:", "value": created_year_str, "inline": True},
                {"name": ":last_quarter_moon: Last Online:", "value": last_online_date_str, "inline": True},
                {"name": ":white_check_mark: Verified:", "value": verified_status, "inline": True},
                {"name": ":dollar: Total RAP:", "value": user_rap, "inline": True},
                {"name": ":hammer: Banned:", "value": f"{isbanned}", "inline": True}, 
                {"name": ":space_invader: Common Passwords:", "value": f"``{roblox_username}123, {roblox_username}{created_year_str}, {roblox_username}s123, {roblox_username}1, {roblox_username}12, {roblox_username}101, qwerty, abc123, password, password123, 12345, 123456789, 1234567``", "inline": True}
            ],
            "footer": {
                "text": f"{version} | made by kellyhated"
            }
        }

        data = {"embeds": [embed]}
        async with session.post(webhook_url, json=data) as response:
            if response.status == 204:
                total_scraped += 1
                
                Logger.info(Fore.GREEN + f" Successfully sent {roblox_username} to webhook | Total Users Scraped: {total_scraped}")
            else:
                Logger.error(Fore.RED + f" Failed to send {roblox_username} to webhook | Status Code: {response.status}")
                asyncio.create_task(clear_output())              

async def clear_output():
    await asyncio.sleep(1.2)
    os.system('cls' if os.name == 'nt' else 'clear')               

async def run():
    webhook = config.get("webhook_url")
    min_id = config.get("min_userid_to_snipe")
    max_id = config.get("max_userid_to_snipe")

    while True:
        try:
            await main(webhook, min_id, max_id)
        except Exception as e:
            Logger.error(Fore.RED + f" An error occurred: {e}")
        await asyncio.sleep(1)

async def setup():
    await run()

if __name__ == "__main__":
    asyncio.run(setup())
