# Generate Passwords
import random
# Useful for data manipulation
import csv
# Cryptography + Using a master password
from cryptography.fernet import Fernet
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# GUI
import PySimpleGUI as sg
import pandas as pd

# Generating initial key
# If a first time use or wishing to start completely fresh, can uncomment for the first runthrough
# Must ensure gen.key does not exist first
'''
def write_key():
    key = Fernet.generate_key()
    with open("gen.key", "wb") as key_file:
        key_file.write(key)
write_key()
'''

# Getting master password
layout = [[sg.Text('Enter Master Password:')],
         [sg.InputText(key='mpwd')],
         [sg.Text('NOTE: If there are no credentials saved any password will work,')],
         [sg.Text('when a credential is added, the password used to login must be used again.')],
         [sg.Button('Submit'), sg.Button('Quit')]]
windowLogin = sg.Window('Login', layout)
event, values = windowLogin.read()
# Exit case
if event == sg.WIN_CLOSED or event == 'Quit':
    exit()
windowLogin.close()
# Extracting password
mPwd = values['mpwd']

# Loading pregenerated key
file = open("gen.key", "rb")
load_key = file.read()
file.close

# Deciphering key
kdf=PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=load_key,
    iterations=390000,
)
key_base = base64.urlsafe_b64encode(kdf.derive(bytes(mPwd, 'ascii')))
key = Fernet(key_base)

# A rudimentary password check, returns invalid token, exits application if password is incorrect once password has been set
with open('passwords.txt', 'r') as f:
    for line in f.readlines():
        text = key.decrypt(line.encode()).decode()

# While loop encapsulating program
marker = True
while marker == True:
    # Main window presenting actions
    layoutMain = [[sg.Text('What would you like to do?')],
                    [sg.Button('Add'), sg.Button('View'), sg.Button('Exit')],
                    [sg.Text('View will not work if no credentials are stored yet')]
                 ] 

    windowMain = sg.Window('Main Panel', layoutMain)

    # Event loop
    while True:
        eventMain, valuesMain = windowMain.read()

        # Exit case, ends both while loops and program
        if eventMain == sg.WIN_CLOSED or eventMain == 'Exit':
            marker = False
            break

        # Add case presents a new gui to enter credentials
        if eventMain == 'Add':
            layout = [
                [sg.Text('Add new account details')],
                [sg.Text('Platform'), sg.InputText(key='platform')],
                [sg.Text('Username'), sg.InputText(key='username')],
                [sg.Text('Password'), sg.InputText(key='password'), sg.Button('Generate')],
                [sg.Text('', key='error')],
                [sg.Button('Add'), sg.Button('Cancel')]
            ]
            windowAdd = sg.Window('Add Credentials', layout)

            # Event loop
            while True:
                eventAdd, valuesAdd = windowAdd.read()

                # Exit case
                if eventAdd == sg.WIN_CLOSED or eventAdd == 'Cancel':
                    break

                # Feature to generate password, creates another new gui
                if eventAdd == 'Generate':
                    layoutGen = [ 
                        # Slider restricts values to integers
                        [sg.Text('Password Length'), sg.Slider(range=(1, 50), orientation='h', key='length')],
                        # Checkbox default to true because more likely to be used
                        [sg.CBox('Use Characters', key='characters', default=True)],
                        [sg.CBox('Use Numbers', key='numbers', default=True)],
                        [sg.CBox('Use Symbols', key='symbols', default=True)],
                        [sg.Text('NOTE: Password will be copied into input upon closing this screen.')],
                        [sg.Text('Password: '), sg.InputText('Password will appear here', key='genpassword'), sg.Button('Generate')],
                        [sg.Button('Close')]
                    ]       
                    windowGen = sg.Window('Generate Password', layoutGen)

                    # Event loop
                    while True:
                        eventGen, valuesGen = windowGen.read()

                        # Exit case
                        if eventGen == sg.WIN_CLOSED or eventGen == 'Close':
                            # In exit case, write password into input on previous screen
                            if valuesGen['genpassword'] != 'Password will appear here':
                                windowAdd['password'].update(valuesGen['genpassword'])

                            break

                        # Generate password
                        if eventGen == 'Generate':

                            # In case pool to create password is empty
                            if valuesGen['characters'] is False and valuesGen['numbers'] is False and valuesGen['symbols'] is False:
                                windowGen['genpassword'].update('Invalid Password, select more options')
                            else:
                                # Set scope of password pool
                                pwdChars = ""

                                # Check for and add various categories to pool
                                if valuesGen['characters'] is True:
                                    pwdChars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                if valuesGen['numbers'] is True:
                                    pwdChars += "0123456789"
                                if valuesGen['symbols'] is True:
                                    pwdChars += "~`!@#$%^&*()_-+={[}]\:;"
                                
                                # Set scope of create password
                                pwdGen = ""

                                # Randomly select from pool and iteratively generate password
                                for i in range(0,int(valuesGen['length'])):
                                    pwdChar = random.choice(pwdChars)
                                    pwdGen = pwdGen + pwdChar

                                # Update text on generate screen to show password
                                windowGen['genpassword'].update(pwdGen)
                    windowGen.close()

                # Securely add password to text file
                if eventAdd == 'Add':
                    # Check to make sure | is not contained within any credentials
                    if ("|" in valuesAdd['platform']) == True or ("|" in valuesAdd['username']) == True or ("|" in valuesAdd['password']) == True:
                        windowAdd['error'].update('Error: "|" can not be contained within any credentials')
                    else:
                        # Open file
                        with open('passwords.txt', 'a') as f:
                            # Combine credentials into a single string
                            text = valuesAdd['platform'] + "|" + valuesAdd['username'] + "|" + valuesAdd['password']
                            # Encrypt string and write into file with a line break following it
                            f.write(key.encrypt(text.encode()).decode() + "\n")
                        break
            windowAdd.close()

        # View all stored credentials
        if eventMain == 'View':
            # Check to ensure file is not empty
            filesize = os.path.getsize("passwords.txt")
            if filesize != 0:
                # Decrypt each line
                with open('passwords.txt', 'r') as f:
                    for line in f.readlines():
                        
                        text = key.decrypt(line.encode()).decode()
                        
                        # Clean up text
                        account = text.rstrip()
                        plat, user, pwd = account.split("|")

                        # Write decrypted text into a csv for easy manipulation into a table
                        with open('passwords.csv', 'a') as f1:
                            writer = csv.writer(f1)
                            writer.writerow([plat, user, pwd])  
                
                # Create values for table
                data = []
                header_list = ['Platform', 'Username', 'Password']
                df = pd.read_csv('passwords.csv', sep=',', engine='python', header=None)
                data = df.values.tolist()

                # Generate table
                layoutView = [
                    [sg.Table(values=data,
                            headings=header_list,
                            display_row_numbers=False,
                            auto_size_columns=False,
                            key='table',
                            hide_vertical_scroll=True,
                            num_rows=min(25, len(data)))],
                    [sg.InputText('Values of selected row will be shown here', key='selectedRow'), sg.Button('Choose row', key='chooseRow')],
                    [sg.Text('If table is not updated, close and reopen this window.')],
                    [sg.Button('Close')]
                ]

                windowView = sg.Window('View Accounts', layoutView, grab_anywhere=False)

                # Event loop
                while True:
                    # Exit case
                    eventView, valuesView = windowView.read()
                    if eventView == sg.WIN_CLOSED or eventView == 'Close':
                        # For security purposes, empty plain text csv file, only leaving encrypted data
                        file = 'passwords.csv'
                        with open('passwords.csv', 'r+') as f:
                            f.truncate(0)

                        break

                    # Make credentials copyable
                    if eventView == 'chooseRow':
                        data_selected = [data[row] for row in valuesView['table']]
                        string = ' '.join([str(item) for item in data_selected])
                        windowView['selectedRow'].update(string)

                windowView.close()
    windowMain.close()