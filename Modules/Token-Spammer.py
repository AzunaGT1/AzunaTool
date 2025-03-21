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

def spam_messages(token, channel_id, message, number):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"content": message}

    for _ in range(number):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return False  
        time.sleep(0.5)  

    return True

def get_friends_list(token):
    url = "https://discord.com/api/v10/users/@me/relationships"
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [friend["id"] for friend in response.json() if friend["type"] == 1]  
    return []

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

            print("\nOption Spammer:")
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Server")
            print(f"├─ {Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} DM")
            spam_choice = input("└──> ").strip()

            if spam_choice in ["1", "01"]:
                server_id = input(f"{Fore.BLUE}Server ID         :{Fore.RESET} ").strip()
                channel_id = input(f"{Fore.BLUE}Channel ID        :{Fore.RESET} ").strip()
                message = input(f"{Fore.BLUE}Message           :{Fore.RESET} ").strip()
                number = input(f"{Fore.BLUE}Number of messages:{Fore.RESET} ").strip()

                try:
                    number = int(number)
                    if number <= 0:
                        print(f"{Fore.RED}The number of messages must be greater than 0.{Fore.RESET}")
                        time.sleep(1)
                        return False
                except ValueError:
                    print(f"{Fore.RED}Invalid number, please enter a valid integer.{Fore.RESET}")
                    time.sleep(1)
                    return False

                success = spam_messages(selected_token, channel_id, message, number)

                if success:
                    print(f"{Fore.GREEN}Successfully spammed the messages.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}An error occurred while spamming messages.{Fore.RESET}")

                time.sleep(1)
                return False

            elif spam_choice in ["2", "02"]:
                print("\nOption DM:")
                print(f"┌─ {Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Specific Friends")
                print(f"├─ {Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} All Friends")
                dm_choice = input("└──> ").strip()

                if dm_choice in ["1", "01"]:
                    friends_ids = input(f"{Fore.BLUE}Friends IDs       :{Fore.RESET} ").strip().split(", ")
                    message = input(f"{Fore.BLUE}Message           :{Fore.RESET} ").strip()
                    number = input(f"{Fore.BLUE}Number of messages:{Fore.RESET} ").strip()

                    try:
                        number = int(number)
                        if number <= 0:
                            print(f"{Fore.RED}The number of messages must be greater than 0.{Fore.RESET}")
                            time.sleep(1)
                            return False
                    except ValueError:
                        print(f"{Fore.RED}Invalid number, please enter a valid integer.{Fore.RESET}")
                        time.sleep(1)
                        return False

                    for friend_id in friends_ids:
                        success = spam_messages(selected_token, friend_id, message, number)
                        if success:
                            print(f"{Fore.GREEN}Message sent to Friend ID: {friend_id}{Fore.RESET}")
                        else:
                            print(f"{Fore.RED}Failed to send message to Friend ID: {friend_id}{Fore.RESET}")

                elif dm_choice in ["2", "02"]:
                    friends_list = get_friends_list(selected_token)
                    if not friends_list:
                        print(f"{Fore.RED}No friends found on this account.{Fore.RESET}")
                        time.sleep(1)
                        return False

                    message = input(f"{Fore.BLUE}Message           :{Fore.RESET} ").strip()
                    number = input(f"{Fore.BLUE}Number of messages:{Fore.RESET} ").strip()

                    try:
                        number = int(number)
                        if number <= 0:
                            print(f"{Fore.RED}The number of messages must be greater than 0.{Fore.RESET}")
                            time.sleep(1)
                            return False
                    except ValueError:
                        print(f"{Fore.RED}Invalid number, please enter a valid integer.{Fore.RESET}")
                        time.sleep(1)
                        return False

                    for friend_id in friends_list:
                        success = spam_messages(selected_token, friend_id, message, number)
                        if success:
                            print(f"{Fore.GREEN}Message sent to Friend ID: {friend_id}{Fore.RESET}")
                        else:
                            print(f"{Fore.RED}Failed to send message to Friend ID: {friend_id}{Fore.RESET}")

                else:
                    print(f"{Fore.RED}Invalid option, please try again.{Fore.RESET}")
                    time.sleep(1)
                    return False

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