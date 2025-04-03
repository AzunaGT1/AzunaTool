import requests
import re
import time
from colorama import *

def delete_webhook(webhook_url):
    match = re.match(r'https://discord.com/api/webhooks/(?P<id>\d+)/(?P<token>[\w-]+)', webhook_url)
    if not match:
        print(f"{Fore.RED}Invalid URL.")
        time.sleep(1)
        return False
    
    response = requests.delete(webhook_url)
    
    if response.status_code == 204:
        print(f"{Fore.GREEN}Webhook successfully removed!")
        time.sleep(1)
        return False
    elif response.status_code == 404:
        print(f"{Fore.RED}Webhook not found. It may have already been deleted.")
        time.sleep(1)
        return False
    elif response.status_code == 401:
        print(f"{Fore.RED}Unauthorized access. Check the webhook URL.")
        time.sleep(1)
        return False
    else:
        print(f"{Fore.RED}Deletion failed. Error code: {response.status_code}")
        time.sleep(1)
        return False
        
if __name__ == "__main__":
    webhook_url = input(f"{Fore.BLUE}Webhook URL:{Fore.RESET} ")
    delete_webhook(webhook_url)