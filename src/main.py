from core.shared import serviceSelection, closeProgram
from search.google.google import googlSearch
import visuals.banner
import os
from dotenv import load_dotenv
import pathlib

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
        elif choice == '2':
            print("Recon feature coming soon.")
        elif choice == '9':
            closeProgram()
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    start()
