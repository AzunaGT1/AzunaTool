import os
import time
import subprocess

os.system("title AzunaTool │ Setup")
print("Installing modules for the AzunaTool:\n")
subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"])
subprocess.run(["python", "-m", "pip", "install", "-r", "requirements.txt"])
print("\nModules installed successfully, launching AzunaTool")
time.sleep(1)
subprocess.run(["python", "AzunaTool.py"])