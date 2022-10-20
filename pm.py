import argparse
import cipher
import os
import secrets
import string
import random
from fileManager import File

VAULT_FILE_NAME = "pv"


def create():
    try:
        open(VAULT_FILE_NAME, mode="x").close()
    except FileExistsError:
        print("Password vault already created")
        return

    vault_file = File(VAULT_FILE_NAME)

    # First write in salt for url hash
    url_salt = os.urandom(32)
    vault_file.write_bin(url_salt)

    master_password = input("Enter your master password: ")

    pub_key, private_key = cipher.gen_rsa()

    # Write public key
    vault_file.write_bin(pub_key)

    # Write in salt for generating vault key from master key
    salt = os.urandom(32)
    vault_file.write_bin(salt)

    vk = cipher.gen_vkey(master_password, salt)

    # Write encrypted private key
    vault_file.write_bin(cipher.aes_enc(private_key, vk))

    vault_file.close()
    print("Password vault created.")


def add():
    if not os.path.isfile(VAULT_FILE_NAME):
        print("Password vault not exist, please check.")
        return

    vault_file = File(VAULT_FILE_NAME)
    salt = vault_file.read_next_bin()
    pub_key = vault_file.read_next_bin()

    url = input("Website URL or note of the entry: ")
    username = input("Username: ")
    pw = input("Password: ")

    url_hash = cipher.hash_url(url, salt)
    un_enc = cipher.rsa_enc(username + url, pub_key)
    pw_enc = cipher.rsa_enc(pw + url, pub_key)

    vault_file.prepare_write()
    vault_file.write_bin(url_hash)
    vault_file.write_bin(un_enc)
    vault_file.write_bin(pw_enc)
    vault_file.close()

    print(url + " saved.")


def search():
    if not os.path.isfile(VAULT_FILE_NAME):
        print("Password vault not exist, please check.")
        return

    vault_file = File(VAULT_FILE_NAME)
    salt = vault_file.read_next_bin()
    vault_file.skip()  # Skip pub key
    pw_salt = vault_file.read_next_bin()
    private_enc = vault_file.read_next_bin()

    url = input("Website URL or note of the entry: ")
    url_hash = cipher.hash_url(url, salt)

    records = []
    entry = vault_file.read_next_bin()
    while len(entry) > 0:
        if entry == url_hash:
            records.append([vault_file.read_next_bin(), vault_file.read_next_bin()])
        else:
            vault_file.skip()
            vault_file.skip()

        entry = vault_file.read_next_bin()

    if len(records) == 0:
        print("No entry found in password vault.")
        return

    master_password = input(f"{len(records)} entry found, type in your master password to decrypt, press enter to "
                            f"cancel: ")
    if len(master_password) == 0:
        print("Decrypt canceled.")
        exit(1)

    vk = cipher.gen_vkey(master_password, pw_salt)
    private_key = cipher.aes_dec(private_enc, vk)

    for un_enc, pw_enc in records:
        try:
            username = cipher.rsa_dec(un_enc, private_key)
            password = cipher.rsa_dec(pw_enc, private_key)
        except ValueError:
            print("Incorrect master password.")
            return
        print(username[:-len(url)] + " : " + password[:-len(url)])


## basic pseudorandom password generation
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

        if (any(char in special_chars for char in pwd) and any(char in number for char in pwd)):
            break

    print("Your password suggestion is: " + pwd)


## our proposed password generation function, based on user's profile
def generatePW2():
    petName, favTeacher, favCity = "", "", ""
    companyID, telephone, birthday = 0, 0, 0
    favEmoji = ""

    charPool = []
    numPool = []

    petName, favTeacher, favCity = input(
        "What is your first petname, name of your favourite teacher and your favourite city?").split(" ")
    companyID, telephone, birthday = input(
        "What is your companyID, a telephone number in your mind, and a birthday in your mind?").split(" ")
    favEmoji = input("What is your favorite emoji? ")

    charPool.extend([petName, favTeacher, favCity])
    numPool.extend([companyID, telephone, birthday])
    # print(charPool)
    # print(numPool)

    suggestion = []

    for i in range(5):
        charPool_index, numPool_index = random.randint(0,2), random.randint(0,2)
        suggestion = [charPool[charPool_index], numPool[numPool_index],favEmoji]
        random.shuffle(suggestion)
        print("".join(suggestion))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["c", "a", "l", "g", "ag"],
                        help="[c]reate new password vault, [a]dd new record, [l]ookup record, [g]enerate password, " +
                             "[a]dvanced [g]enerate password")
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
