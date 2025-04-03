import requests
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

LANGUAGES = {
    "01": ("en-US", "English"),
    "02": ("fr", "French"),
    "03": ("es-ES", "Spanish"),
    "04": ("de", "German"),
    "05": ("it", "Italian"),
    "06": ("ru", "Russian"),
    "07": ("ja", "Japanese"),
    "08": ("zh-CN", "Chinese (Simplified)"),
    "09": ("ko", "Korean"),
}

def get_user_info(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("username"), data.get("locale", "Unknown")
    else:
        return None, None  

def update_language(token, new_language):
    url = "https://discord.com/api/v10/users/@me/settings"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"locale": new_language}

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
    username, language = get_user_info(token)
    if username:
        return (token, username, language)
    else:
        return None

def display_tokens(valid_tokens):
    if not valid_tokens:
        print(f"{Fore.RED}You have not put any token, you cannot use this option.{Fore.RESET}")
        time.sleep(1)
        return False
    else:
        for index, (token, username, language) in enumerate(valid_tokens, start=1):
            print(f"┌─ {Fore.BLUE}[{Fore.RESET}{index:02d}{Fore.BLUE}]{Fore.RESET} {username}")

        choice = input(f"└──> {Fore.RESET}")

        try:
            choice = int(choice)
            if 1 <= choice <= len(valid_tokens):
                selected_token, selected_username, current_language = valid_tokens[choice - 1]

                print("\nAvailable Languages:")
                for num, (code, lang) in LANGUAGES.items():
                    print(f"{Fore.BLUE}[{Fore.RESET}{num}{Fore.BLUE}]{Fore.RESET} {lang}")

                current_lang_name = next((lang for code, lang in LANGUAGES.values() if code == current_language), "Unknown")
                print(f"\n{Fore.BLUE}Current Language:{Fore.RESET} {current_lang_name}")

                new_lang_choice = input(f"{Fore.BLUE}New Language    :{Fore.RESET} ")

                if new_lang_choice in LANGUAGES or f"{int(new_lang_choice):02d}" in LANGUAGES:
                    new_language_code = LANGUAGES.get(f"{int(new_lang_choice):02d}")[0]
                    success = update_language(selected_token, new_language_code)

                    if success:
                        print(f"{Fore.GREEN}Successfully updated language to:{Fore.RESET} {LANGUAGES[f'{int(new_lang_choice):02d}'][1]}")
                    else:
                        print(f"{Fore.RED}An error has occurred while updating the language.{Fore.RESET}")

                    time.sleep(1)
                    return False
                else:
                    print(f"{Fore.RED}Invalid language option, please try again.{Fore.RESET}")
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
