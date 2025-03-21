import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("username")
    return None

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
    return (token, username) if username else None

def get_friends_list(token):
    url = "https://discord.com/api/v10/users/@me/relationships"
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [friend["id"] for friend in response.json() if friend["type"] == 1]  
    return []

def block_friend(token, friend_id):
    url = f"https://discord.com/api/v10/users/@me/relationships/{friend_id}"
    headers = {
        "Authorization": token,
    }
    response = requests.put(url, headers=headers, json={"type": 2})  

    if response.status_code == 204:
        return True  
    else:
        return False  

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False

    for index, (token, username) in enumerate(valid_tokens, start=1):
        print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

    choice = input(f"└──> {Fore.RESET}")

    try:
        choice = int(choice)
        if 1 <= choice <= len(valid_tokens):
            selected_token, selected_username = valid_tokens[choice - 1]

            print("\nOption to block friends:")
            print("┌─ [01] Specific Friends")
            print("├─ [02] All Friends")
            friend_choice = input("└──> ").strip()

            if friend_choice in ["1", "01"]:
                friend_ids = input(f"{Fore.BLUE}Enter Friend IDs:{Fore.RESET} ").strip().split(", ")
                
                for friend_id in friend_ids:
                    success = block_friend(selected_token, friend_id.strip())
                    if success:
                        print(f"{Fore.GREEN}Successfully blocked Friend ID:{Fore.RESET} {friend_id}")
                    else:
                        print(f"{Fore.RED}Failed to block Friend ID:{Fore.RESET} {friend_id}")

            elif friend_choice in ["2", "02"]:
                friends_list = get_friends_list(selected_token)
                if not friends_list:
                    print(f"{Fore.RED}No friends found on this account.{Fore.RESET}")
                    time.sleep(1)
                    return False

                print(f"{Fore.GREEN}Blocking all friends...{Fore.RESET}")
                for friend_id in friends_list:
                    success = block_friend(selected_token, friend_id)
                    if success:
                        print(f"{Fore.GREEN}Successfully blocked Friend ID:{Fore.RESET} {friend_id}")
                    else:
                        print(f"{Fore.RED}Failed to block Friend ID:{Fore.RESET} {friend_id}")

                time.sleep(1)
                return False

            else:
                print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
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