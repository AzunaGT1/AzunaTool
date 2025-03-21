import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        username = data.get("username")
        return username
    else:
        return None

def check_tokens(file_path):
    with open(file_path, "r") as file:
        tokens = file.readlines()

    valid_tokens = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(process_token, token.strip()) for token in tokens]

        for future in futures:
            result = future.result()
            if result:
                valid_tokens.append(result)

    return valid_tokens

def process_token(token):
    username = get_user_info(token)
    if username:
        return (token, username)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, username) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

        choice = input(f"└──> {Fore.RESET}")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username = valid_tokens[choice - 1]

                delete_dm_option(selected_token)
                return True
            else:
                print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
                time.sleep(1)
                return False
        except ValueError:
            print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
            time.sleep(1)
            return False

def delete_dm_option(token):
    print("\nOption:")
    print(f"┌─ {Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Specific Friends")
    print(f"├─ {Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} All Open DMs")
    option = input(f"└──> {Fore.RESET}")

    if option in ['1', '01']:
        friend_ids = input(f"{Fore.BLUE}Friends IDs:{Fore.RESET} ").strip()
        delete_specific_dms(token, friend_ids)
    
    elif option in ['2', '02']:
        delete_all_dms(token)
    
    else:
        print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
        time.sleep(1)
        return False

def delete_specific_dms(token, friend_ids):
    friend_ids_list = friend_ids.split(',')
    success_count = 0
    failed_count = 0

    for friend_id in friend_ids_list:
        response = close_dm(token, friend_id.strip())
        if response:
            success_count += 1
        else:
            failed_count += 1

        time.sleep(0.5)  

    print(f"{Fore.GREEN}Successfully deleted {success_count} DMs.{Fore.RESET}")
    print(f"{Fore.RED}Failed to delete {failed_count} DMs.{Fore.RESET}")
    time.sleep(1)
    return False

def delete_all_dms(token):
    success_count = 0
    failed_count = 0

    dms = get_open_dms(token)

    for dm in dms:
        response = close_dm(token, dm['id'])
        if response:
            success_count += 1
        else:
            failed_count += 1

        time.sleep(0.5)  

    print(f"{Fore.GREEN}Successfully deleted {success_count} DMs.{Fore.RESET}")
    print(f"{Fore.RED}Failed to delete {failed_count} DMs.{Fore.RESET}")
    time.sleep(1)
    return False

def close_dm(token, dm_id):
    url = f"https://discord.com/api/v10/channels/{dm_id}"
    headers = {
        "Authorization": token
    }
    
    response = requests.delete(url, headers=headers)
    return response.status_code == 200

def get_open_dms(token):
    url = "https://discord.com/api/v10/users/@me/channels"
    headers = {
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

if __name__ == "__main__":
    file_path = "TokenDisc.txt"
    valid_tokens = check_tokens(file_path)
    while True:
        if not display_tokens(valid_tokens):
            break