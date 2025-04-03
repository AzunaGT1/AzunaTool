import requests
import time
from colorama import *
from concurrent.futures import ThreadPoolExecutor
from datetime import *

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"{Fore.RED}Failed to fetch user info for token: {token}{Fore.RESET}")
        return None

def get_user_connections(token):
    url = "https://discord.com/api/v10/users/@me/connections"
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_user_guilds(token):
    url = "https://discord.com/api/v10/users/@me/guilds"
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_tokens(file_path):
    try:
        with open(file_path, "r") as file:
            tokens = file.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}File not found: {file_path}{Fore.RESET}")
        return False

    valid_tokens = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(process_token, token.strip()) for token in tokens]

        for future in futures:
            result = future.result()
            if result:
                valid_tokens.append(result)

    return valid_tokens if valid_tokens else False

def process_token(token):
    user_data = get_user_info(token)
    if user_data:
        return token, user_data
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any valid token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    
    for index, (token, _) in enumerate(valid_tokens, start=1):
        user_data = valid_tokens[index - 1][1]  
        username = user_data.get('username', 'Unknown')
        print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

    choice = input(f"└──>{Fore.RESET} ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(valid_tokens):
            selected_token, _ = valid_tokens[choice - 1]
            return selected_token
        else:
            print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
            time.sleep(1)
            return False
    except ValueError:
        print(f"{Fore.RED}Invalid option, please enter a number.{Fore.RESET}")
        time.sleep(1)
        return False

def display_user_info(user_data, token):
    try:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_data.get('id')}/{user_data.get('avatar')}.png"
        banner_url = f"https://cdn.discordapp.com/banners/{user_data.get('id')}/{user_data.get('banner')}.png" if user_data.get('banner') else "No banner URL"
        username = user_data.get('username', 'Unknown')

        print(f"{username}'s Information:")
        print(f"{Fore.BLUE}Token                 :{Fore.RESET} {token}")
        print(f"{Fore.BLUE}User ID               :{Fore.RESET} {user_data.get('id')}")
        print(f"{Fore.BLUE}Descriminator         :{Fore.RESET} {user_data.get('discriminator')}")
        print(f"{Fore.BLUE}Username              :{Fore.RESET} {user_data.get('username')}")
        print(f"{Fore.BLUE}Display Name          :{Fore.RESET} {user_data.get('global_name', 'No display name')}")
        print(f"{Fore.BLUE}Avatar URL            :{Fore.RESET} {avatar_url}")
        print(f"{Fore.BLUE}Banner URL            :{Fore.RESET} {banner_url}")
        print(f"{Fore.BLUE}Email                 :{Fore.RESET} {user_data.get('email', 'No email set')}")
        print(f"{Fore.BLUE}Language              :{Fore.RESET} {user_data.get('locale')}")
        print(f"{Fore.BLUE}Flags                 :{Fore.RESET} {user_data.get('flags')}")
        print(f"{Fore.BLUE}Badges                :{Fore.RESET} {user_data.get('public_flags')}")
        
        premium_type = user_data.get('premium_type', 0)
        if premium_type == 1:
            premium_type_str = "Nitro Basic"
        elif premium_type == 2:
            premium_type_str = "Nitro Boost"
        else:
            premium_type_str = "No Nitro"
        
        print(f"{Fore.BLUE}Prenium Type          :{Fore.RESET} {premium_type_str}")
        
        print(f"{Fore.BLUE}Current Boost(s)      :{Fore.RESET} {user_data.get('premium_type', 'No Boost')}")

        account_creation_timestamp = int(user_data.get('id', 0)) // 4194304 + 1420070400000
        account_creation = datetime.fromtimestamp(account_creation_timestamp / 1000, timezone.utc).strftime('%d/%m/%Y %H:%M:%S')
        print(f"{Fore.BLUE}Account Creation Date :{Fore.RESET} {account_creation}")
        
        mfa_enabled = 'Enabled' if user_data.get('mfa_enabled') else 'Disabled'
        print(f"{Fore.BLUE}Multi-Factor Auth     :{Fore.RESET} {mfa_enabled}")
        
        phone_number = user_data.get('phone', 'No phone number set')
        print(f"{Fore.BLUE}Phone Number          :{Fore.RESET} {phone_number}")

        connections = get_user_connections(token)
        if connections:
            print(f"{Fore.BLUE}Connection Information:{Fore.RESET}")
            for conn in connections:
                print(f"   {conn.get('type')} - {conn.get('name')}")

        presence = user_data.get('presence', {}).get('status', 'No presence data')
        print(f"{Fore.BLUE}Presence              :{Fore.RESET} {presence}")

        custom_status = user_data.get('custom_status', {}).get('text', 'No custom status')
        print(f"{Fore.BLUE}Custom Status         :{Fore.RESET} {custom_status}")

        activity = user_data.get('activity', {}).get('name', 'No activity data')
        print(f"{Fore.BLUE}Activity              :{Fore.RESET} {activity}")

        guilds = get_user_guilds(token)
        if guilds:
            guild_names = [guild['name'] for guild in guilds if guild.get('owner')]
            print(f"{Fore.BLUE}Guild Owner           :{Fore.RESET} {len(guild_names)} | {', '.join(guild_names)}")
        else:
            print(f"{Fore.BLUE}Guild Owner           :{Fore.RESET} No guilds")

        if connections:
            friends = [conn.get('name') for conn in connections if conn.get('type') == 'discord']
            if friends:
                print(f"{Fore.BLUE}Friends               :{Fore.RESET} {', '.join(friends)}")
            else:
                print(f"{Fore.BLUE}Friends               :{Fore.RESET} No friends data")
        else:
            print(f"{Fore.BLUE}Friends               :{Fore.RESET} No friends data")

        input(f"\nPress Enter to return to the main menu...{Fore.RESET}")
        return True
    except Exception as e:
        print(f"{Fore.RED}An error occurred while retrieving the user information: {e}{Fore.RESET}")
        return False

def main():
    file_path = "TokenDisc.txt"
    valid_tokens = check_tokens(file_path)
    
    if not valid_tokens:
        print(f"{Fore.RED}No valid tokens found.{Fore.RESET}")
        return

    selected_token = False
    while not selected_token:
        selected_token = display_tokens(valid_tokens)
        if selected_token is False:
            return

    user_data = get_user_info(selected_token)
    if user_data:
        success = display_user_info(user_data, selected_token)
        if not success:
            print(f"{Fore.RED}An error occurred displaying user data.{Fore.RESET}")
    else:
        print(f"{Fore.RED}Failed to retrieve user data. Exiting...{Fore.RESET}")
        return

if __name__ == "__main__":
    main()