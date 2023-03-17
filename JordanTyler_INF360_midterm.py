# INF360 - Programming in Python
# Jordan Tyler
# Midterm

'''
Put desciption of project here
'''

"""
TODO: 
- Improve look of menu
- Add a log.txt file
    - Add a log to log.txt after every file manipulation function. 
    - Add a the current time/date to each keep track of timelines.
- Add a readlogRecent function to output 25 most recent logs
- Add a readLogs function to output all logs 
- Create readStorage function that reads all files from all bins in storage directory

"""

import os
import shutil
import sys
import re


def displayMenu():
    print("File utility Application")
    menu = '''Move file - 1 (Moves a given file from one location to another)
    Create new text file - 2 
    Read files from directory - 3 
    Delete a file - 4
    Exit - 0'''
    print(menu)


# Create storage location if one does not exist
def createStorageLocation():
    # Build directory paths
    storage = os.path.join(os.path.curdir, 'storage')
    bins = ['bin1', 'bin2', 'bin3', 'bin4', 'bin5']
    paths = []

    for bin in bins:
        paths.append(os.path.join(storage, bin))
    bin1, bin2, bin3, bin4, bin5 = paths

    # Store directories
    directories = {
        'storage': {
        'path': storage,
        'exists': False
        }, 
        'bin1': {
        'path': bin1,
        'exists': False
        },
        'bin2': {
        'path': bin2,
        'exists': False
        },
        'bin3': {
        'path': bin3,
        'exists': False
        },
        'bin4': {
        'path': bin4,
        'exists': False
        },
        'bin5': {
        'path': bin5,
        'exists': False
        }
    }
    
    # Check if directory exists
    for pathInfo in directories.values():
        pathInfo['exists'] = pathExists(pathInfo['path'])

    # If directory not present, add it
    for x in directories:
        if(directories[x]['exists'] == False):
            os.mkdir(directories[x]['path'])
            #TODO Add log of added directories


# Get user input
def getInput(prompt = '', isPath= False):
    result = input(prompt)
    if (isPath):
        result = result.replace('"', '')
    return result


# Run selected function, check for valid input
def userSelection(choice):
    match choice:
        case "1": 
            moveFile()
        case "2":
            createTextFile()
        case "3":
            readFromDir()
        case "4":
            deleteFile()
        case "0":
            print("Exit Confirmed")
            sys.exit()
        case _:
            print("Error - menu choice \"" + choice + "\" is invalid.")
            userSelection(getInput())


# Move a file or directory at source to destination
def moveFile():
    src = getSourceDirectory()
    dest = getDestinationDirectory()
    try:
        movedTo = shutil.move(src, dest)
        print("\nSuccessfully moved", src, "to destination", movedTo)

    except Exception as e:
        print("Error during file move. Exception Error: ", e)


# Checks if path exists
def pathExists(path):
    return os.path.exists(path)


# Asks user for source directory 
def getSourceDirectory():
    while(True):
        path = getInput("Enter a valid source path >> ", True)
        if (pathExists(path)):
            break
        print("Error, source path invalid")
    return path


# Asks user for destination directory 
def getDestinationDirectory():
    while(True):
        path = getInput("Enter a valid destination path >> ", True)
        if (pathExists(path)): 
            break
        print("Error, destination path invalid")
    return path


# Create new text file 
def createTextFile():
    #TODO add brief description to user on how to use this function
    location = fileRegex = '' 

    # Validate user input for file name
    while(not fileRegex):
        fileName = getInput("Enter file name without extension (.txt) >> ")
        fileRegex = re.findall('^[A-Za-z0-9&_-]{1,25}$', fileName)
        if(not fileRegex):
            print('File name invalid.')
    fileName += '.txt' # Add txt extension 

    while(not pathExists(location)):
        location = getInput("Enter a valid path for new file >> ", True)

    # Create new file
    with open(os.path.join(location, fileName), 'w') as f:
        f.close()
    print(f"\nFile {fileName} was created at {location}")


# Outputs directories and file names from given directory
def readFromDir():
    # Get valid directory path
    while (True):
        path = getInput("Enter a directory path to read >> ", True)
        if (os.path.isdir(path)):
            break
        print("Error not a valid directory")
    print(f'\n{os.listdir(path)}')


# Deletes a file from a given location
def deleteFile():
    while(True):
        path = getInput("Enter the file path of the file to delete >> ", True)
        if (os.path.isfile(path) and pathExists(path)):
            break
        elif (not os.path.isfile(path)):
            print("Error, given path is not a file")
        elif (not pathExists(path)):
            print('Error, given path does not exist')
    os.remove(path)
    print(f"\nFile at {path} has successfully been removed")


def main():
    createStorageLocation()
    while (True):
        displayMenu()
        userSelection(getInput("Enter choice here >> "))
        print()

main()