import requests
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

def get_username(token):
    headers = {
        "Authorization": token
    }
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data["username"]
    else:
        return None

def update_username(token, new_username):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "username": new_username
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return True
    else:
        return False

def check_tokens(file_path):
    with open(file_path, "r") as file:
        tokens = file.readlines()
    
    valid_tokens = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for token in tokens:
            token = token.strip()
            futures.append(executor.submit(process_token, token))
        
        for future in futures:
            result = future.result()
            if result:
                valid_tokens.append(result)
    
    return valid_tokens

def process_token(token):
    username = get_username(token)
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
                print(f"{Fore.BLUE}Current Username:{Fore.RESET} {selected_username}")
                new_username = input(f"{Fore.BLUE}New Username    :{Fore.RESET} ")
                success = update_username(selected_token, new_username)
                
                if success:
                    print(f"{Fore.GREEN}Successfully updated username to:{Fore.RESET} {new_username}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the username.{Fore.RESET}")                
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