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
        avatar_url = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png" if data.get('avatar') else "No Avatar"
        return username, avatar_url
    else:
        return None, None  

def update_avatar(token, image_url):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"avatar": image_url}

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
    username, avatar_url = get_user_info(token)
    if username:
        return (token, username, avatar_url)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, username, avatar_url) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

        choice = input(f"└──> {Fore.RESET}")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username, current_avatar = valid_tokens[choice - 1]
                print(f"{Fore.BLUE}Current Avatar URL:{Fore.RESET} {current_avatar}")
                new_avatar_url = input(f"{Fore.BLUE}New Avatar URL    :{Fore.RESET} ").strip()

                if not new_avatar_url.startswith("http"):
                    print(f"{Fore.RED}Invalid URL. Please provide a valid URL.{Fore.RESET}")
                    time.sleep(1)
                    return False

                valid_extensions = ['.gif', '.png', '.jpeg', '.jpg']
                if not any(new_avatar_url.lower().endswith(ext) for ext in valid_extensions):
                    print(f"{Fore.RED}Invalid file format. Please use gif, png, jpeg, or jpg.{Fore.RESET}")
                    time.sleep(1)
                    return False

                success = update_avatar(selected_token, new_avatar_url)

                if success:
                    print(f"{Fore.GREEN}Successfully updated avatar to:{Fore.RESET} {new_avatar_url}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the avatar.{Fore.RESET}")

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
