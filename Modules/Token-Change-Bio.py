import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("username"), data.get("bio", "No bio set")
    else:
        return None, None 

def update_bio(token, new_bio):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"bio": new_bio}

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
    username, bio = get_user_info(token)
    if username:
        return (token, username, bio)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, username, bio) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

        choice = input(f"└──>{Fore.RESET} ")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username, current_bio = valid_tokens[choice - 1]
                print(f"{Fore.BLUE}Current Bio:{Fore.RESET} {current_bio}")
                new_bio = input(f"{Fore.BLUE}New Bio    :{Fore.RESET} ")
                success = update_bio(selected_token, new_bio)

                if success:
                    print(f"{Fore.GREEN}Successfully updated bio to:{Fore.RESET} {new_bio}")
                else:
                    print(f"{Fore.RED}An error has occurred while updating the bio.{Fore.RESET}")

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