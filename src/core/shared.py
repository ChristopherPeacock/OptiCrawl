import sys

def closeProgram():
    sys.exit()

def serviceSelection():
    print("Select a service to use:")
    print("1. Google Search")
    print("2. Recon")
    print("3. E.V.A")
    print("9. Close Program")

def dnsChecker(url):
    return url