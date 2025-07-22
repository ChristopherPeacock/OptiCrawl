from search.google.automationSearch import serpapi
from tools.emailScraper import loadListAndExtract
from core.shared import closeProgram, serviceSelection

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

def findKeyWord():
    keyWord = input("Enter the search keyword:")
    return keyWord

def findLocation():
    location = input("Enter the location (e.g., United States):")
    return location

def googlSearch():
    searchKeyWord = input("Enter the search keyword: ")
    location = findLocation()
    success = serpapi(searchKeyWord, location, 'google')
    if success == -1:
        print('No new Urls was found')
        serviceSelection()
    if success == 1:
        whatToDoWithData()

if __name__ == 'main':
    googlSearch()