from colorama import Fore, Style
import requests
import time

def check_webhook(webhook_url):
    response = requests.get(webhook_url)
    
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        print(f"{Fore.RED}Invalid webhook URL. Please enter a valid one.{Style.RESET_ALL}")
        time.sleep(1)
        return False
    else:
        print(f"{Fore.RED}Error verifying webhook. Please try again.{Style.RESET_ALL}")
        time.sleep(1)
        return False

webhook = input(f"{Fore.BLUE}Webhook URL    :{Fore.RESET} ")
if not check_webhook(webhook):
    exit()
message = input(f"{Fore.BLUE}Message        :{Fore.RESET} ")

while True:
    try:
        count = int(input(f"{Fore.BLUE}Number of Times:{Fore.RESET} "))
        if count <= 0:
            print(f"{Fore.RED}Invalid number, please try again.{Style.RESET_ALL}")
            time.sleep(1)
            continue
        break
    except ValueError:
        print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        time.sleep(1)

for i in range(count):
    response = requests.post(webhook, json={"content": message})
    if response.status_code == 204:
        print(f"{Fore.GREEN}Message {Style.RESET_ALL}{i + 1}/{count}{Fore.GREEN} sent successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Failed to send message {Style.RESET_ALL}{i + 1}/{count}.")
        exit()
    time.sleep(1)  

input(f"{Fore.RESET}Press 'Enter' to return to main.")
time.sleep(1)
exit()