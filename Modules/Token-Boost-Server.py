import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        nitro_boosts = data.get("premium_type", 0)  
        return data.get("username"), nitro_boosts
    else:
        return None, None  

def boost_server(token, server_id, boosts):
    url = f"https://discord.com/api/v10/guilds/{server_id}/premium/subscriptions"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    for _ in range(boosts):
        response = requests.post(url, headers=headers)

        if response.status_code != 201:
            return False  

    return True  

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
    username, nitro_boosts = get_user_info(token)
    if username and nitro_boosts > 0:
        return (token, username, nitro_boosts)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, username, nitro_boosts) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

        choice = input(f"└──> {Fore.RESET}")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username, available_boosts = valid_tokens[choice - 1]
                if available_boosts == 0:
                    print(f"{Fore.RED}You have no Nitro boosts available.{Fore.RESET}")
                    time.sleep(1)
                    return False

                print(f"{Fore.BLUE}Remaining Boosts       :{Fore.RESET} {available_boosts}")                   
                server_id = input(f"{Fore.BLUE}Server ID              :{Fore.RESET} ").strip()                   
                number_of_boosts = input(f"{Fore.BLUE}Number of Boosts to add:{Fore.RESET} ").strip()     

                try:
                    number_of_boosts = int(number_of_boosts)
                    if number_of_boosts > available_boosts:
                        print(f"{Fore.RED}You cannot add more boosts than you have available.{Fore.RESET}")
                        time.sleep(1)
                        return False
                    
                    success = boost_server(selected_token, server_id, number_of_boosts)

                    if success:
                        print(f"{Fore.GREEN}Successfully boosted the server.{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}An error has occurred while boosting the server.{Fore.RESET}")

                    time.sleep(1)
                    return False
                except ValueError:
                    print(f"{Fore.RED}Invalid number of boosts, please try again.{Fore.RESET}")
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