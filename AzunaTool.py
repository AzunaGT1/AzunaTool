import os
import requests
import fade
import time
import getpass
from concurrent.futures import ThreadPoolExecutor
import subprocess
from colorama import *

def validtoken(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def verif_tokens(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    with ThreadPoolExecutor(max_workers=100) as executor:  
        valid_tokens = list(executor.map(validtoken, (ligne.strip() for ligne in lines)))

    vtoken_count = sum(valid_tokens)
    return vtoken_count

file = 'TokenDisc.txt'

vtoken_count = verif_tokens(file)

print(vtoken_count)

def check_for_update():
    try:
        latest = requests.get("https://api.github.com/repos/AzunaGT1/AzunaTool/releases/latest", timeout=5).json().get("tag_name")
        if latest and latest != "V1.0":
            print(f"{Fore.CYAN}New Version{Fore.WHITE} | {Fore.WHITE}──> {Fore.CYAN}{latest}")
        else:
            return
    except requests.RequestException:
        pass

def numtoken(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    token_count = sum(1 for ligne in lines if ligne.strip())
    
    return token_count

file = 'TokenDisc.txt'
tokenc = numtoken(file)

def clear():
  os.system("cls" if os.name == "nt" else "clear")

username = getpass.getuser()

def Azuna1():
    clear()
    os.system("title AzunaTool │ Menu 1")
    gui = f"""
                                  ▄████████  ▄███████▄  ███    █▄  ███▄▄▄▄      ▄████████ 
                                 ███    ███ ██▀     ▄██ ███    ███ ███▀▀▀██▄   ███    ███ 
                                 ███    ███       ▄███▀ ███    ███ ███   ███   ███    ███ 
                                 ███    ███  ▀█▀▄███▀▄▄ ███    ███ ███   ███   ███    ███ 
                               ▀███████████   ▄███▀   ▀ ███    ███ ███   ███ ▀███████████ 
                                 ███    ███ ▄███▀       ███    ███ ███   ███   ███    ███ 
                                 ███    ███ ███▄     ▄█ ███    ███ ███   ███   ███    ███ 
                                 ███    █▀   ▀████████▀ ████████▀   ▀█   █▀    ███    █▀  
                                                                                                                                           
                                            {Fore.BLUE}╔════════════════════════════════╗
                                            {Fore.BLUE}║{Fore.RESET}  Token: {tokenc:<3} | {Fore.RESET}Valid Token:{Fore.GREEN} {vtoken_count:>2}  {Fore.BLUE}║
                                            {Fore.BLUE}╚════════════════════════════════╝
  
            {Fore.BLUE}[{Fore.RESET}01{Fore.BLUE}]{Fore.RESET} Token Change Username         {Fore.BLUE}[{Fore.RESET}11{Fore.BLUE}]{Fore.RESET} Token Create Group            {Fore.BLUE}[{Fore.RESET}21{Fore.BLUE}]{Fore.RESET} Token Nuker
            {Fore.BLUE}[{Fore.RESET}02{Fore.BLUE}]{Fore.RESET} Token Change Display Name     {Fore.BLUE}[{Fore.RESET}12{Fore.BLUE}]{Fore.RESET} Token Join Group              {Fore.BLUE}[{Fore.RESET}22{Fore.BLUE}]{Fore.RESET} Webhook Spammer
            {Fore.BLUE}[{Fore.RESET}03{Fore.BLUE}]{Fore.RESET} Token Change Language         {Fore.BLUE}[{Fore.RESET}13{Fore.BLUE}]{Fore.RESET} Token Leave Group             {Fore.BLUE}[{Fore.RESET}23{Fore.BLUE}]{Fore.RESET} Webhook Information
            {Fore.BLUE}[{Fore.RESET}04{Fore.BLUE}]{Fore.RESET} Token Change Status           {Fore.BLUE}[{Fore.RESET}14{Fore.BLUE}]{Fore.RESET} Token Join Discord Server     {Fore.BLUE}[{Fore.RESET}24{Fore.BLUE}]{Fore.RESET} Wehhook Delete
            {Fore.BLUE}[{Fore.RESET}05{Fore.BLUE}]{Fore.RESET} Token Change Profile Picture  {Fore.BLUE}[{Fore.RESET}15{Fore.BLUE}]{Fore.RESET} Token Leave Discord Server    {Fore.BLUE}[{Fore.RESET}25{Fore.BLUE}]{Fore.RESET} Token Information
            {Fore.BLUE}[{Fore.RESET}06{Fore.BLUE}]{Fore.RESET} Token Change Bio              {Fore.BLUE}[{Fore.RESET}16{Fore.BLUE}]{Fore.RESET} Token Delete Friends          {Fore.BLUE}[{Fore.RESET}26{Fore.BLUE}]{Fore.RESET} Token Grabber File
            {Fore.BLUE}[{Fore.RESET}07{Fore.BLUE}]{Fore.RESET} Token Change Theme            {Fore.BLUE}[{Fore.RESET}17{Fore.BLUE}]{Fore.RESET} Token Block Friends           {Fore.BLUE}[{Fore.RESET}27{Fore.BLUE}]{Fore.RESET} Token Boost Server
            {Fore.BLUE}[{Fore.RESET}08{Fore.BLUE}]{Fore.RESET} Token Change House            {Fore.BLUE}[{Fore.RESET}18{Fore.BLUE}]{Fore.RESET} Token Mass DM                 {Fore.BLUE}[{Fore.RESET}28{Fore.BLUE}]{Fore.RESET} 
            {Fore.BLUE}[{Fore.RESET}09{Fore.BLUE}]{Fore.RESET} Token Change Custom Status    {Fore.BLUE}[{Fore.RESET}19{Fore.BLUE}]{Fore.RESET} Token Delete DM               {Fore.BLUE}[{Fore.RESET}29{Fore.BLUE}]{Fore.RESET} 
            {Fore.BLUE}[{Fore.RESET}10{Fore.BLUE}]{Fore.RESET} Token Change Banner           {Fore.BLUE}[{Fore.RESET}20{Fore.BLUE}]{Fore.RESET} Token Spammer                 {Fore.BLUE}[{Fore.RESET}30{Fore.BLUE}]{Fore.RESET} 
"""
    for line in str(fade.water(gui)).split("\n"):  
        print(line)
        time.sleep(0.01)
    
    while True:
        choice = input(f"{Fore.BLUE}┌─({Fore.RESET}{username}@AzunaTool{Fore.BLUE})\n└──>{Fore.RESET} ")
        
        if choice in['01', '1', '02', '2', '03', '3', '04', '4', '05', '5', '06', '6', '07', '7','08', '8', '09', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']:
          if choice in option:
            subprocess.run(['python', option[choice]])
            clear()  
            for line in str(fade.water(gui)).split("\n"):  
                print(line)
                time.sleep(0.01)
        else:
            print(f"{Fore.RED}Invalid choice, please try again.{Fore.RESET}")
            time.sleep(1)
            clear()  
            for line in str(fade.water(gui)).split("\n"):  
                print(line)
                time.sleep(0.01)

option = {
    "1": "Modules/Token-Change-Username.py",
    "01": "Modules/Token-Change-Username.py",
    "2": "Modules/Token-Change-Display-Name.py",
    "02": "Modules/Token-Change-Display-Name.py",
    "3": "Modules/Token-Change-Language.py",
    "03": "Modules/Token-Change-Language.py",
    "4": "Modules/Token-Change-Status.py",
    "04": "Modules/Token-Change-Status.py",
    "5": "Modules/Token-Change-PFP.py",
    "05": "Modules/Token-Change-PFP.py",
    "6": "Modules/Token-Change-Bio.py",
    "06": "Modules/Token-Change-Bio.py",
    "7": "Modules/Token-Change-Theme.py",
    "07": "Modules/Token-Change-Theme.py",
    "8": "Modules/Token-Change-House.py",
    "08": "Modules/Token-Change-House.py",
    "9": "Modules/Token-Change-Custom-Status.py",
    "09": "Modules/Token-Change-Custom-Status.py",
    "10": "Modules/Token-Change-Banner.py",
    "11": "Modules/Token-Create-Group.py",
    "12": "Modules/Token-Join-Group.py",
    "13": "Modules/Token-Leave-Group.py",
    "14": "Modules/Token-Join-Discord-Server.py",
    "15": "Modules/Token-Leave-Discord-Server.py",
    "16": "Modules/Token-Delete-Friends.py",
    "17": "Modules/Token-Block-Friends.py",
    "18": "Modules/Token-Mass-DM.py",
    "19": "Modules/Token-Delete-DM.py",
    "20": "Modules/Token-Spammer.py",
    "21": "Modules/Token-Nuker.py",
    "22": "Modules/Webhook-Spammer.py",
    "23": "Modules/Webhook-Info.py",
    "24": "Modules/Webhook-Delete.py",
    "25": "Modules/Token-Info.py",
    "26": "Modules/Token-Grabber.py",
    "27": "Modules/Token-Boost-Server.py"
}

Azuna1()