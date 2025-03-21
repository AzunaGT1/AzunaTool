import requests
import time
from colorama import init, Fore

LEAVE_GROUP_URL = "https://discord.com/api/v10/users/@me/guilds/{}"

def get_username(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        return response.json().get("username")
    else:
        return None 

def leave_group(token, guild_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    response = requests.delete(LEAVE_GROUP_URL.format(guild_id), headers=headers)
    
    return response.status_code == 204  

def check_tokens(file_path):
    with open(file_path, "r") as file:
        tokens = file.readlines()

    valid_tokens = []
    for token in tokens:
        token = token.strip()
        username = get_username(token)
        if username:
            valid_tokens.append((token, username))

    return valid_tokens

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False

    for index, (token, username) in enumerate(valid_tokens, start=1):
        print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

    choice = input(f"└──> {Fore.RESET}")

    try:
        choice = int(choice)
        if 1 <= choice <= len(valid_tokens):
            selected_token = valid_tokens[choice - 1][0]
            return leave_group_menu(selected_token)
        else:
            print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
            time.sleep(1)
            return False
    except ValueError:
        print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
        time.sleep(1)
        return False

def leave_group_menu(token):
    guild_id = input(f"{Fore.BLUE}Group ID:{Fore.RESET} ").strip()
    
    if not guild_id.isdigit():
        print(f"{Fore.RED}Invalid Group ID. Please enter a valid numerical ID.{Fore.RESET}")
        time.sleep(1)
        return False

    success = leave_group(token, guild_id)

    if success:
        print(f"{Fore.GREEN}Successfully left the group!{Fore.RESET}")
    else:
        print(f"{Fore.RED}An error has occurred while leaving the group.{Fore.RESET}")

    time.sleep(1)
    return False 

if __name__ == "__main__":
    file_path = "TokenDisc.txt"
    valid_tokens = check_tokens(file_path)
    while True:
        if not display_tokens(valid_tokens):
            break
