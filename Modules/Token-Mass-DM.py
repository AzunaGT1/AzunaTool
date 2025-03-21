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

                mass_dm_option(selected_token)
                return True
            else:
                print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
                time.sleep(1)
                return False
        except ValueError:
            print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
            time.sleep(1)
            return False

def mass_dm_option(token):
    print("\nOption:")
    print(f"┌─ {Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Specific Friends")
    print(f"├─ {Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} All Friends")
    option = input(f"└──>{Fore.RESET} ")

    if option in ['1', '01']:
        friend_ids = input(f"{Fore.BLUE}Friends IDs       :{Fore.RESET} ").strip()
        message = input(f"{Fore.BLUE}Message           :{Fore.RESET} ").strip()
        number_per_message = int(input(f"{Fore.BLUE}Number Per Message:{Fore.RESET} ").strip())
        send_mass_dm_specific(token, friend_ids, message, number_per_message)
    
    elif option in ['2', '02']:
        message = input(f"{Fore.BLUE}Message           :{Fore.RESET} ").strip()
        number_per_message = int(input(f"{Fore.BLUE}Number Per Message:{Fore.RESET} ").strip())
        send_mass_dm_all(token, message, number_per_message)
    
    else:
        print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
        time.sleep(1)
        return False

def send_mass_dm_specific(token, friend_ids, message, number_per_message):
    friend_ids_list = friend_ids.split(',')
    success_count = 0
    failed_count = 0

    for friend_id in friend_ids_list:
        response = send_dm(token, friend_id.strip(), message)
        if response:
            success_count += 1
        else:
            failed_count += 1

        time.sleep(number_per_message / 100)  

    print(f"{Fore.GREEN}Successfully sent {success_count} messages.{Fore.RESET}")
    print(f"{Fore.RED}Failed to send {failed_count} messages.{Fore.RESET}")
    time.sleep(1)
    return False    

def send_mass_dm_all(token, message, number_per_message):
    success_count = 0
    failed_count = 0

    friends = get_friends(token)

    for friend in friends:
        response = send_dm(token, friend['id'], message)
        if response:
            success_count += 1
        else:
            failed_count += 1

        time.sleep(number_per_message / 1000)  

    print(f"{Fore.GREEN}Successfully sent {success_count} messages.{Fore.RESET}")
    print(f"{Fore.RED}Failed to send {failed_count} messages.{Fore.RESET}")
    time.sleep(1)
    return False

def send_dm(token, friend_id, message):
    url = "https://discord.com/api/v10/users/@me/channels"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "recipient_id": friend_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        channel_id = response.json()['id']
        dm_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        message_data = {
            "content": message
        }
        message_response = requests.post(dm_url, headers=headers, json=message_data)
        if message_response.status_code == 200:
            return True 
    return False 

def get_friends(token):
    url = "https://discord.com/api/v10/users/@me/relationships"
    headers = {
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

if __name__ == "__main__":
    file_path = "TokenDisc.txt"
    valid_tokens = check_tokens(file_path)
    while True:
        if not display_tokens(valid_tokens):
            break
