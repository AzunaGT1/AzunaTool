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

def get_current_hypesquad(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/hypesquad/online", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("house", "no_house")  
    else:
        return None

def set_hypesquad(token, house):
    url = "https://discord.com/api/v10/hypesquad/online"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "house": house
    }

    response = requests.post(url, headers=headers, json=data)
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
                
                print(f"\n{Fore.BLUE}Available House:{Fore.RESET}")
                print(f"{Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} HypeSquad Bravery")
                print(f"{Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} HypeSquad Brilliance")
                print(f"{Fore.BLUE}[{Fore.RESET}03{Fore.BLUE}]{Fore.RESET} HypeSquad Balance")

                print(f"\n{Fore.BLUE}Current House:{Fore.RESET} {get_current_hypesquad(selected_token)}")

                new_house = input(f"{Fore.BLUE}New House   :{Fore.RESET} ").strip()
 
                if new_house not in ["1", "01", "2", "02", "3", "03"]:
                    print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
                    time.sleep(1)
                    return False

                house_dict = {
                    "1": "bravery",
                    "01": "bravery",
                    "2": "brilliance",
                    "02": "brilliance",
                    "3": "balance",
                    "03": "balance"
                }

                house = house_dict[new_house]
                success = set_hypesquad(selected_token, house)

                if success:
                    print(f"{Fore.GREEN}Successfully updated HypeSquad house to:{Fore.RESET} {house}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the house.{Fore.RESET}")

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