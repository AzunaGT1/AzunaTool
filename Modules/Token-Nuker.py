import requests
import time
from colorama import *
from concurrent.futures import ThreadPoolExecutor

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("username"), data.get("status", "No status set")
    else:
        return None, None

def update_status(token, new_status):
    url = "https://discord.com/api/v10/users/@me/settings"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"custom_status": {"text": new_status}}

    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200

def update_theme_and_language(token, theme, language):
    url = "https://discord.com/api/v10/users/@me/settings"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "theme": theme,
        "locale": language
    }

    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200

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
    username, status = get_user_info(token)
    if username:
        return (token, username, status)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any valid token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    
    for index, (token, username, status) in enumerate(valid_tokens, start=1):
        print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

    choice = input(f"└──>{Fore.RESET} ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(valid_tokens):
            selected_token, _, _ = valid_tokens[choice - 1]
            return selected_token
        else:
            print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
            time.sleep(1)
            return False
    except ValueError:
        print(f"{Fore.RED}Invalid option, please enter a number.{Fore.RESET}")
        time.sleep(1)
        return False

def print_status(theme, language, status):
    status_display = f"{Fore.BLUE}Custom Status:{Fore.RESET} {status}" if status else ""
    print(f"{Fore.BLUE}Theme:{Fore.RESET} {theme:<5} │ {Fore.BLUE}Language:{Fore.RESET} {language:<5} │ {status_display}")

def loop_process(selected_token, num_loops):
    languages = ["zh-CN", "zh-TW", "ar", "ko", "ja", "fi", "hu", "ka", "is", "eu"]
    themes = ["Dark", "Light"]
    
    for loop in range(num_loops):
        for i in range(10):
            theme = themes[i % 2]  
            language = languages[i % len(languages)]  

            status = "Nuked By AzunaTool" if i < 5 else "https://github.com/AzunaGT1/AzunaTool"

            if not update_status(selected_token, status) or not update_theme_and_language(selected_token, theme.lower(), language):
                print(f"{Fore.RED}Failed to update Discord settings. Stopping.{Fore.RESET}")
                time.sleep(1)
                return False

            print_status(theme, language, status if i == 0 or i == 5 else "")

            time.sleep(1)
    return True

if __name__ == "__main__":
    file_path = "TokenDisc.txt"
    valid_tokens = check_tokens(file_path)
    
    if not valid_tokens:
        exit()

    selected_token = False
    while not selected_token:
        selected_token = display_tokens(valid_tokens)
        if selected_token is False:
            exit()

    num_loops = 0
    while num_loops <= 0:
        try:
            num_loops = int(input(f"{Fore.BLUE}Number of Loop:{Fore.RESET} "))
            if num_loops <= 0:
                print(f"{Fore.RED}Please enter a positive number.{Fore.RESET}")
                time.sleep(1)
                exit()
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.{Fore.RESET}")
            time.sleep(1)
            exit()

    if not loop_process(selected_token, num_loops):
        exit()