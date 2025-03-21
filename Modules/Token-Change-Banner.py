import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("username"), data.get("banner", None)
    else:
        return None, None  

def update_banner(token, banner_url):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    data = {
        "banner": banner_url 
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
    username, banner = get_user_info(token)
    if username:
        return (token, username, banner)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, username, banner) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

        choice = input(f"└──> {Fore.RESET}")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username, current_banner = valid_tokens[choice - 1]
                if current_banner:
                    print(f"{Fore.BLUE}Current Banner URL:{Fore.RESET} https://cdn.discordapp.com/banners/{selected_token}/{current_banner}")
                else:
                    print(f"{Fore.BLUE}Current Banner:{Fore.RESET} No banner set")
                
                new_banner_url = input(f"{Fore.BLUE}Enter the URL for the new banner image:{Fore.RESET} ").strip()

                if not new_banner_url.lower().startswith(('http://', 'https://')):
                    print(f"{Fore.RED}Invalid URL format. Please provide a valid URL for the banner image.{Fore.RESET}")
                    time.sleep(1)
                    return False

                success = update_banner(selected_token, new_banner_url)

                if success:
                    print(f"{Fore.GREEN}Successfully updated banner.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the banner.{Fore.RESET}")

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