import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

STATUS_OPTIONS = {
    "1": "online",
    "01": "online",
    "2": "invisible",
    "02": "invisible",
    "3": "idle",
    "03": "idle",
    "4": "dnd",
    "04": "dnd"
}

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("username"), data.get("status", "offline")
    else:
        return None, None  

def update_status(token, new_status):
    url = "https://discord.com/api/v10/users/@me/settings"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"status": new_status}

    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200  

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
    username, status = get_user_info(token)
    if username:
        return (token, username, status)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, username, status) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

        choice = input(f"└──> {Fore.RESET}")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username, current_status = valid_tokens[choice - 1]
                
                print("\nAvailable Status:")
                print(f"{Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Online")
                print(f"{Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} Invisible")
                print(f"{Fore.BLUE}[{Fore.RESET}03{Fore.BLUE}]{Fore.RESET} Inactive")
                print(f"{Fore.BLUE}[{Fore.RESET}04{Fore.BLUE}]{Fore.RESET} Do not disturb\n")
                
                print(f"{Fore.BLUE}Current Status:{Fore.RESET} {current_status}")
                new_status_choice = input(f"{Fore.BLUE}New Status    :{Fore.RESET} ").strip()

                if new_status_choice not in STATUS_OPTIONS:
                    print(f"{Fore.RED}Invalid status selection. Please try again.{Fore.RESET}")
                    time.sleep(1)
                    return False

                new_status = STATUS_OPTIONS[new_status_choice]
                success = update_status(selected_token, new_status)

                if success:
                    print(f"{Fore.GREEN}Successfully updated status to:{Fore.RESET} {new_status.capitalize()}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the status.{Fore.RESET}")

                time.sleep(1)
                return False
            else:
                print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
                time.sleep(1)
                return False
        except ValueError:
            print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
            time.sleep(1)
            return False

if __name__ == "__main__":
    file_path = "TokenDisc.txt"
    valid_tokens = check_tokens(file_path)
    while True:
        if not display_tokens(valid_tokens):
            break