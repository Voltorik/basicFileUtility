# INF360 - Programming in Python
# Jordan Tyler
# Midterm

'''
Project Desription:

-File Utility Application-
Provides some file management, creation, and deletion functions.

Storage Info:
A directory "storage" is automatically generated in the current working directory of the program upon execution.
This directory contains 5 additional directories (bin1 - bin5), that can be used to test all functions of this program.
The current working directory is the default when using path inputs, so accessing storage only requires the use of "storage\binNum" as the path. 
To access a file in storage, simply use "storage\binNum\fileName" as the path input.

Functions:
1. moveFile - Moves a specified file or directory to another directory. Takes the source file or directory's path and destination directory's path as input.
2. createTextFile - Creates a new text file at given directory. Takes the file's name and directory's path as input.
3. readFromDir - Outputs all files and directories from a given directory. Takes the directory's path as input.
4. readFromStorage - Outputs all files and directories from the "storage" directory found in the current working directory. "Storage" directory is generated automatically upon running the program.
Also outputs all files and directories inside of bins 1-5. Takes no inputs.
5. deleteFile - Deletes a file from a given file path. Takes the file path for the file to delete as input.

At any time, typing the phrase "go back" will take the user back to the starting menu.
'''

import os, sys, shutil, re


# Output menu
def callMenu():
    print("-----File Utility Application-----")
    menu = ("Guide:\n"\
    "Source directory = the file/folder to move.\n"\
    "Destination directory = the folder to move to.\n"\
    'Enter path in form like "D:\Downloads\\nameOfFile". Path can be copy pasted from clipboard.\n'\
    "There is a built in folder called \"storage\" located in the current working directory that can be used to test these functions.\n"\
    "Type \"go back\" at any time to come back to this menu.\n\n"\
    "Functions:\n"\
    "1 - Move a file from one directory to another\n"\
    "2 - Create a new text file\n"\
    "3 - Read files from a directory\n"\
    "4 - Read files from storage directory\n"\
    "5 - Delete a file\n"\
    "0 - Exit\n\n"\
    "Type the corresponding number as your choice below.\n")
    print(menu)

    userSelection(getInput("Enter choice here >> "))
    print()
    

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


# Get user input
def getInput(prompt = '', isPath = False):
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
            readFromStorage()
        case "5":
            deleteFile()
        case "0":
            print("Exit Confirmed")
            sys.exit()
        case "go back":
            print()
            callMenu()
        case _:
            print("Error - menu choice \"" + choice + "\" is invalid.")
            userSelection(getInput("Enter choice here >> "))
  

# Move a file or directory at source to destination
def moveFile():
    src = getSourceDirectory()
    if (src.lower() == 'go back'):
        userSelection('go back')
    else:
        dest = getDestinationDirectory()
        if (dest.lower() == 'go back'):
            userSelection('go back')
        else:
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
        if (path.lower() == 'go back'):
            break
        elif (pathExists(path)):
            break
        print("Error, source path invalid.") 
    return path


# Asks user for destination directory 
def getDestinationDirectory():
    while(True):
        path = getInput("Enter a valid destination path >> ", True)
        if (path.lower() == 'go back'):
            break
        elif (pathExists(path)): 
            break
        print("Error, destination path invalid.")
    return path


# Create new text file 
def createTextFile():
    location = fileRegex = '' 

    # Validate user input for file name
    while (not fileRegex):
        fileName = getInput("Enter file name without extension (.txt) >> ")
        if (fileName.lower() == 'go back'):
            break
        fileRegex = re.findall('^[A-Za-z0-9&_-]{1,25}$', fileName)
        if (not fileRegex):
            print('File name invalid.')

    if (fileName.lower() == 'go back'):
        userSelection('go back')
    else:
        while (not pathExists(location)):
            location = getInput("Enter a valid path for new file >> ", True)
            if (location.lower() == 'go back'):
                break
            print('Error, not a valid file path.')
        if (location.lower() == 'go back'):
            userSelection('go back')
        else:
            # Create new file
            fileName += '.txt' # Add txt extension 
            with open(os.path.join(location, fileName), 'w') as f:
                f.close()
            print(f"\nFile {fileName} was created at {location}.")


# Outputs directories and file names from given directory
def readFromDir():
    # Get valid directory path
    while (True):
        path = getInput("Enter a directory path to read >> ", True)
        if(path.lower() == 'go back'):
            break
        if (os.path.isdir(path)):
            break
        print("Error not a valid directory.")
    if(path.lower() == 'go back'):
        userSelection('go back')
    else:
        print(f'\n{os.listdir(path)}')


# Outputs all directories and files from the storage directory, including those in bins 1-5
def readFromStorage():
    path = os.path.join(os.getcwd(), 'storage')
    for bin in os.listdir(path):
        print(f'{bin}', end='')
        if (os.path.isdir(os.path.join(path, bin))):
            print(f' -> {os.listdir(os.path.join(path, bin))}')
    print()


# Deletes a file from a given location
def deleteFile():
    while(True):
        path = getInput("Enter the file path of the file to delete >> ", True)
        if (path.lower() == 'go back'):
            break
        elif (os.path.isfile(path) and pathExists(path)):
            break
        elif (not os.path.isfile(path)):
            print("Error, given path is not a file.")
        elif (not pathExists(path)):
            print('Error, given path does not exist.')
    if (path.lower() == 'go back'):
        userSelection('go back')
    else:
        os.remove(path)
        print(f"\nFile at {path} has successfully been removed")


def main():
    createStorageLocation()
    while (True):
        callMenu()
main()