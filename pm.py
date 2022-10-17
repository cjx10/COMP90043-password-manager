import argparse
from os.path import exists
import secrets
import string
import random

VAULT_FILE_NAME = "pv"


def create(vault_file=None):
    try:
        vault_file = open(VAULT_FILE_NAME, mode="x")
    except FileExistsError:
        print("Password vault already created")
        exit(1)

    master_password = input("Enter your master password: ")
    vault_file.write(master_password + '\n')


def add(vault_file=None):
    if not exists(VAULT_FILE_NAME):
        print("Password vault not exist, please check.")
        exit(1)

    vault_file = open(VAULT_FILE_NAME, mode="a")

    # read public key on first line
    # read salt for url on second line
    # exit if error

    url = input("Website URL or note of the entry: ")
    username = input("Username: ")
    pw = input("Password: ")

    # hash url with salt
    # encrypt username+url and pw+url with public key

    vault_file.write(url + "," + username+url + "," + pw+url + '\n')
    vault_file.close()

    print(url + " saved.")


def search(vault_file=None):
    if not exists(VAULT_FILE_NAME):
        print("Password vault not exist, please check.")
        exit(1)

    vault_file = open(VAULT_FILE_NAME, mode="r")

    url = input("Website URL or note of the entry: ")

    # hash url with salt

    records = []
    for line in vault_file.readlines():
        if line.find(url) != -1:
            records.append(line)

    if len(records) == 0:
        print("No entry found in password vault.")
        return

    master_password = input(f"{len(records)} entry found, type in your master password to decrypt, press enter to "
                            f"cancel: ")
    if len(master_password) == 0:
        print("Decrypt canceled.")
        exit(1)

    # decrypt private key using user input
    # try decrypt record with private key, exit if failed

    for record in records:
        items = record.split(",")
        print(items[1][:-len(url)] + " : " + items[2][:-len(url)-1])

def generatePW():
    alphabet = string.ascii_letters
    number = string.digits
    special_chars = string.punctuation

    pool = alphabet + number + special_chars

    pwd_length = 12

    while True:
        pwd = ""
        for i in range(pwd_length):
            pwd += "".join(secrets.choice(pool))

        if(any(char in special_chars for char in pwd) and any(char in number for char in pwd)):
            break;

    print("Your password suggestion is: " + pwd)

def generatePW2():
    petName, favTeacher, favCity = "","",""
    companyID, telephone, birthday = 0,0,0
    favEmoji = ""

    charPool = []
    numPool = []

    petName, favTeacher, favCity = input("What is your first petname, name of your favourite teacher and your favourite city?").split(" ")
    companyID, telephone, birthday = input("What is your companyID, a telephone number in your mind, and a birthday in your mind?").split(" ")
    favEmoji = input("What is your favorite emoji? ")

    charPool.extend([petName, favTeacher, favCity])
    numPool.extend([companyID, telephone, birthday])
    #print(charPool)
    #print(numPool)

    suggestion = []

    for i in range(5):
        charPool_index, numPool_index = random.randint(0,2), random.randint(0,2)
        suggestion = [charPool[charPool_index], numPool[numPool_index],favEmoji]
        print("".join(suggestion))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["c", "a", "l", "g", "ag"],
                        help="[c]reate new password vault, [a]dd new record, [l]ookup record, [g]enerate password, [a]dvanced [g]enerate password")
    parser.add_argument("-f", "--file", help="Password vault file", default="pv")
    args = parser.parse_args()
    VAULT_FILE_NAME = args.file

    if args.operation == "c":
        create()
    if args.operation == "a":
        add()
    if args.operation == "l":
        search()
    if args.operation == "g":
        generatePW()
    if args.operation == "ag":
        generatePW2()
