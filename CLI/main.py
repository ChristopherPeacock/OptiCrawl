from automationSearch import main
from banner import show_banner
import os
import sys
from dotenv import load_dotenv
from emailScraper import loadListAndExtract
import pathlib

def findKeyWord():
    keyWord = input("Enter the search keyword:")
    return keyWord

def findLocation():
    location = input("Enter the location (e.g., United States):")
    return location

def closeProgram():
    return sys.exit()

def whatToDoWithData():
    print("Select what you want to do to the service.")
    print("1. Extract Emails")
    print("2. Extract Phone Numbers")
    print("3. Extract Option 1 and Option 2")
    print("9. Close Program")
    
    decision = input("Enter your choice (1-3): ")
    
    navigation = {
        '1': loadListAndExtract,
        '2': extractPhoneNumber,
        '3': extractPhoneAndEmail,
        '9': closeProgram,
    }
    
    action = navigation.get(decision)
    if action:
        action()
    else:
        print("Invalid selection.")

def extractPhoneNumber():
    print('')
    print("feature unavailable")
    print('')
    whatToDoWithData()
    return

def extractPhoneAndEmail():
    print('')
    print("Service Not Available")
    print('')
    whatToDoWithData()

def serviceSelection():
    print("Select a service to use:")
    
    print("1. Google")
    
    print("9. Close Program")
       
    choice = input("Enter your choice (1-5): ")
    
    if choice == '1':
        engine = 'google'
    elif choice == '9':
        closeProgram()
    else:
        print("Invalid choice, Choose again.")
        serviceSelection()
        
    return engine 

def start():
    api_key_name = 'SERPAPIKEY'
    value = os.environ.get(api_key_name)
    env_path = pathlib.Path("Data/.env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        
        with open("Data/.env", "a") as env_file:
            env_file.write(f"\n{api_key_name}={value}")
        
        os.environ[api_key_name] = value
    else: 
        engine = serviceSelection()
        searchKeyWord = input("Enter the search keyword: ")
        location = findLocation()
        success = main(searchKeyWord, location, engine)
        if success == -1:
            print('No new Urls was found')
            serviceSelection()
        if success == 1:
            whatToDoWithData()
    return   
 
start()
