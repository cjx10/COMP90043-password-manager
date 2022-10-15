import argparse
from os.path import exists

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["c", "a", "l"],
                        help="[c]reate new password vault, [a]dd new record, [l]ookup record")
    parser.add_argument("-f", "--file", help="Password vault file", default="pv")
    args = parser.parse_args()
    VAULT_FILE_NAME = args.file

    if args.operation == "c":
        create()
    if args.operation == "a":
        add()
    if args.operation == "l":
        search()
