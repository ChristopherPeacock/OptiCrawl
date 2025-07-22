from core.shared import serviceSelection, closeProgram
from search.google.google import googlSearch
from recon.main import recon
import visuals.banner 
from visuals.banner import show_banner
import os
from dotenv import load_dotenv
import pathlib
import time

def start():
    api_key_name = 'SERPAPIKEY'
    value = os.environ.get(api_key_name)
    env_path = pathlib.Path("Data/.env")

    if not value:
        print(f"[ERROR] {api_key_name} not found in system environment.")
        closeProgram()

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

        with open(env_path, "r") as env_file:
            existing_lines = env_file.read().splitlines()

        if not any(line.startswith(f"{api_key_name}=") for line in existing_lines):
            with open(env_path, "a") as env_file:
                env_file.write(f"\n{api_key_name}={value}")

        os.environ[api_key_name] = value

    while True:
        serviceSelection()
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            googlSearch()
            print('Data Collected')
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')
            show_banner()
        elif choice == '2':
            recon()
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')
            show_banner()
        elif choice == '3':
            print('E.V.A is coming soon..')
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')
            show_banner()
        elif choice == '9':
            closeProgram()
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    start()
