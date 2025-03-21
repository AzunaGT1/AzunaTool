import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

def get_display_name(token):
    headers = {
        "Authorization": token
    }
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data["username"] 
    else:
        return None

def update_display_name(token, new_display_name):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "username": new_display_name  
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
    display_name = get_display_name(token)
    if display_name:
        return (token, display_name)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, display_name) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {display_name}")
        
        choice = input(f"└──> {Fore.RESET}")
        
        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_display_name = valid_tokens[choice - 1]
                print(f"{Fore.BLUE}Current Display Name:{Fore.RESET} {selected_display_name}")
                new_display_name = input(f"{Fore.BLUE}New Display Name    :{Fore.RESET} ")
                success = update_display_name(selected_token, new_display_name)
                
                if success:
                    print(f"{Fore.GREEN}Successfully updated display name to:{Fore.RESET} {new_display_name}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the display name.{Fore.RESET}")
                
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
