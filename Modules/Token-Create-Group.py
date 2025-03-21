import requests
import time
from colorama import init, Fore

FRIENDS_URL = "https://discord.com/api/v10/users/@me/relationships"
GROUP_URL = "https://discord.com/api/v10/users/@me/channels"

def get_username(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        return response.json().get("username")
    else:
        return None  

def get_friends(token):
    headers = {"Authorization": token}
    response = requests.get(FRIENDS_URL, headers=headers)

    if response.status_code == 200:
        return [friend["id"] for friend in response.json()]
    else:
        return None  

def create_group(token, friend_ids, group_name):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "recipients": friend_ids,
        "name": group_name
    }
    response = requests.post(GROUP_URL, headers=headers, json=data)
    
    return response.status_code == 200  

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
            selected_token, selected_username = valid_tokens[choice - 1]
            return create_group_menu(selected_token, selected_username)
        else:
            print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
            time.sleep(1)
            return False
    except ValueError:
        print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
        time.sleep(1)
        return False

def create_group_menu(token, username):
    print("\nChoose an option:")
    print(f"┌─ {Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Specific Friends")
    print(f"├─ {Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} All Friends")
    choice = input(f"└──> {Fore.RESET}")

    if choice in ["1", "01"]:
        friend_ids_input = input(f"{Fore.BLUE}Friends IDs     :{Fore.RESET} ")
        friend_ids = [fid.strip() for fid in friend_ids_input.split(", ")]

        if not all(fid.isdigit() for fid in friend_ids):
            print(f"{Fore.RED}Invalid friend ID(s). Please enter valid numeric IDs.{Fore.RESET}")
            time.sleep(1)
            return False

    elif choice in ["2", "02"]:
        friend_ids = get_friends(token)
        if not friend_ids:
            print(f"{Fore.RED}Failed to retrieve friends list.{Fore.RESET}")
            time.sleep(1)
            return False
    else:
        print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
        time.sleep(1)
        return False

    group_name = input(f"{Fore.BLUE}Name Of Group   :{Fore.RESET} ").strip()
    if not group_name:
        print(f"{Fore.RED}Group name cannot be empty.{Fore.RESET}")
        time.sleep(1)
        return False

    number_of_groups = input(f"{Fore.BLUE}Number Of Groups:{Fore.RESET} ").strip()
    if not number_of_groups.isdigit() or int(number_of_groups) <= 0:
        print(f"{Fore.RED}Invalid number of groups. Please enter a valid number.{Fore.RESET}")
        time.sleep(1)
        return False

    number_of_groups = int(number_of_groups)

    for _ in range(number_of_groups):
        success = create_group(token, friend_ids, group_name)
        if not success:
            print(f"{Fore.RED}An error has occurred while creating the group.{Fore.RESET}")
            time.sleep(1)
            return False

    print(f"{Fore.GREEN}Successfully created {number_of_groups} group(s) named '{group_name}'.{Fore.RESET}")
    time.sleep(1)
    return False

if __name__ == "__main__":
    file_path = "TokenDisc.txt"
    valid_tokens = check_tokens(file_path)
    while True:
        if not display_tokens(valid_tokens):
            break