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

def get_current_theme(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me/settings", headers=headers)

    if response.status_code == 200:
        settings = response.json()
        return settings.get("theme", "dark")  
    else:
        return None

def set_theme(token, theme):
    url = "https://discord.com/api/v10/users/@me/settings"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "theme": theme
    }

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

        print(f"\n{Fore.BLUE}Available Theme:{Fore.RESET}")
        print(f"{Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Dark")
        print(f"{Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} Light\n")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username = valid_tokens[choice - 1]
                print(f"{Fore.BLUE}Current Theme:{Fore.RESET} {get_current_theme(selected_token)}")
                
                new_theme = input(f"{Fore.BLUE}New Theme    :{Fore.RESET} ").strip()

                if new_theme not in ["1", "01", "2", "02"]:
                    print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
                    time.sleep(1)
                    return False

                theme = "dark" if new_theme in ["1", "01"] else "light"
                success = set_theme(selected_token, theme)

                if success:
                    print(f"{Fore.GREEN}Successfully updated theme to:{Fore.RESET} {theme}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the theme.{Fore.RESET}")

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