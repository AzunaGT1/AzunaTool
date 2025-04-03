import requests
from datetime import *
import re
import time
from colorama import *

def get_webhook_info(webhook_url):
    match = re.match(r'https://discord.com/api/webhooks/(?P<id>\d+)/(?P<token>[\w-]+)', webhook_url)
    if not match:
        print(f"{Fore.RED}Invalid URL.")
        time.sleep(1)
        return False
    
    response = requests.get(webhook_url)
    if response.status_code == 200:
        data = response.json()
        
        webhook_id = data.get("id", "N/A")
        token = match.group("token")
        name = data.get("name", "N/A")
        avatar_url = f'https://cdn.discordapp.com/avatars/{webhook_id}/{data["avatar"]}.png' if data.get("avatar") else "N/A"
        webhook_type = "Incoming" if data.get("type") == 1 else "Unknown"
        server_id = data.get("guild_id", "N/A")
        channel_id = data.get("channel_id", "N/A")
        creator_id = data.get("user", {}).get("id", "N/A")
        
        timestamp = (int(webhook_id) >> 22) + 1420070400000
        creation_time = datetime.fromtimestamp(timestamp / 1000).strftime('Date: %m/%d/%Y Hour: %H:%M:%S')
        
        print(f"\n{Fore.BLUE}ID           :{Fore.RESET} {webhook_id}")
        print(f"{Fore.BLUE}Token        :{Fore.RESET} {token}")
        print(f"{Fore.BLUE}Name         :{Fore.RESET} {name}")
        print(f"{Fore.BLUE}Avatar URL   :{Fore.RESET} {avatar_url}")
        print(f"{Fore.BLUE}Type         :{Fore.RESET} {webhook_type}")
        print(f"{Fore.BLUE}Server ID    :{Fore.RESET} {server_id}")
        print(f"{Fore.BLUE}Channel ID   :{Fore.RESET} {channel_id}")
        print(f"{Fore.BLUE}Creator ID   :{Fore.RESET} {creator_id}")
        print(f"{Fore.BLUE}Creation Time:{Fore.RESET} {creation_time}\n")
    else:
        print(f"{Fore.RED}Unable to retrieve webhook information. Check the URL and try again.")
        time.sleep(1)
        return False

    input("Press 'Enter' to return to the main.")
    time.sleep(1)
    return False

if __name__ == "__main__":
    webhook_url = input(f"{Fore.BLUE}Webhook URL:{Fore.RESET} ")
    get_webhook_info(webhook_url)