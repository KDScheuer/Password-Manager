import os.path
import tkinter as tk
from tkinter import Tk
import hashlib
from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_dict = {}

    def first_run(self, password):
        """Generates a key, master key and password file"""
        hashed = hashlib.sha512(password.encode()).hexdigest()
        with open("auth.key", "w") as f:
            f.write(str(hashed))

        self.key = Fernet.generate_key()
        with open("key.key", 'wb') as f:
            f.write(self.key)
        with open("passwords.pass", "w"):
            pass

        main_menu()

    def load_key_and_passwords(self):
        """Loads the created key and password file"""
        with open("key.key", 'rb') as f:
            self.key = f.read()

        with open("passwords.pass", 'r') as f:
            for line in f:
                site, encrypted_username, encrypted_password = line.split(":")
                self.password_dict[site] = [Fernet(self.key).decrypt(encrypted_username.encode()).decode(),
                                            Fernet(self.key).decrypt(encrypted_password.encode()).decode()]

    def add_password(self, site, username, password):
        """Adds a Site, Username, and Password to the Password File"""
        self.password_dict[site] = [username, password]
        self.save_pass_dict()
        main_menu()

    def delete_account(self, app):
        """Deletes the Username and Password of the specified Site from the Password File"""
        self.password_dict = {site: value for (site, value) in self.password_dict.items() if site != app}
        self.save_pass_dict()
        main_menu()

    def modify_account(self, app, username, password):
        """Modifies the Username and Password of the specified Site"""
        self.password_dict = {site: value for (site, value) in self.password_dict.items() if site != app}
        self.password_dict[app] = [username, password]
        self.save_pass_dict()
        main_menu()

    def save_pass_dict(self):
        """Saves the Password Dictionary to the Password File"""
        with open("passwords.pass", 'w') as f:
            for key in self.password_dict:
                site = key
                username = self.password_dict[key][0]
                password = self.password_dict[key][1]
                encrypted_username = Fernet(self.key).encrypt(username.encode())
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted_username.decode() + ":" + encrypted_password.decode() + "\n")
        main_menu()


pm = PasswordManager()
gui = Tk()


def clearscreen():
    for widget in gui.winfo_children():
        widget.destroy()


def add_account():
    """Prompts for account name and passes results to modify function for username and password"""
    clearscreen()
    label = tk.Label(gui, text="Add Account", bg="gray", fg="black", width="400", font=("Ariel", 20))
    account_frame = tk.Frame(gui, bg="lightblue")
    account_label = tk.Label(account_frame, text="Account Name", bg="lightblue", fg="black", width=17)
    account_entry = tk.Entry(account_frame, bg="lightgray", fg="black", width=25)
    submit_btn = tk.Button(gui, text="Submit", command=lambda: modify_account(account_entry.get()))
    menu_btn = tk.Button(gui, text="Main Menu", command=main_menu)

    label.pack()
    account_label.pack(side="left", padx=5)
    account_entry.pack(side="right")
    account_frame.pack(pady=20)
    submit_btn.pack()
    menu_btn.pack(pady=10)


def modify_account(site):
    """Prompts for new username and password for account"""
    clearscreen()
    label = tk.Label(gui, text=site, bg="gray", fg="black", width=400, font=("Ariel", 20))
    user_frame = tk.Frame(gui, bg="lightblue")
    user_label = tk.Label(user_frame, text="Username ", bg="lightblue", fg="black", width=15)
    user_entry = tk.Entry(user_frame, bg="lightgray", fg="black", width=30)
    pass_frame = tk.Frame(gui, bg="lightblue")
    pass_label = tk.Label(pass_frame, text="Password ", bg="lightblue", fg="black", width=15)
    pass_entry = tk.Entry(pass_frame, bg="lightgray", fg="black", width=30)
    submit_btn = tk.Button(gui, text="Submit",
                           command=lambda: pm.modify_account(site, user_entry.get(), pass_entry.get()))
    menu_btn = tk.Button(gui, text="Main Menu", command=main_menu)

    label.pack()
    user_label.pack(side="left", padx=5)
    user_entry.pack(side="right")
    user_frame.pack(pady=10)
    pass_label.pack(side="left", padx=5)
    pass_entry.pack(side="right")
    pass_frame.pack(pady=10)
    submit_btn.pack(pady=10)
    menu_btn.pack(pady=10)


def account_info(site, username, password):
    """Displays account info and prompts for modification / deletion of account"""
    clearscreen()
    label = tk.Label(gui, text=site, bg="gray", fg="black", width=400, font=("Ariel", 20))
    user_label = tk.Label(gui, text=username, bg="lightblue", fg="black")
    password_label = tk.Label(gui, text=password, bg="lightblue", fg="black")
    btn_frame = tk.Frame(gui, bg="lightblue")
    modify_btn = tk.Button(btn_frame, text="Modify", command=lambda: modify_account(site))
    delete_btn = tk.Button(btn_frame, text="Delete", command=lambda: pm.delete_account(site))
    menu_btn = tk.Button(gui, text="Main Menu", command=main_menu)

    label.pack()
    user_label.pack(pady=10)
    password_label.pack(pady=10)
    modify_btn.pack(side="right", padx=10)
    delete_btn.pack(side="left")
    btn_frame.pack(pady=20)
    menu_btn.pack()


def accounts():
    """Displays List of all account in Password File"""
    clearscreen()
    label = tk.Label(gui, text="Accounts", width=400, bg="gray", fg="black", font=("Ariel", 20))
    label.pack()

    for key in pm.password_dict:
        btn = tk.Button(gui, text=key, width=30, command=lambda key1=key: account_info(key1, pm.password_dict[key1][0],
                                                                                       pm.password_dict[key1][1]))
        btn.pack(pady=10)

    menu_btn = tk.Button(gui, text="Main Menu", command=main_menu)
    menu_btn.pack(pady=10)


def main_menu():
    """Displays the Main Menu"""
    clearscreen()
    label = tk.Label(gui, text="Main Menu", width=400, bg="gray", fg="black", font=("Ariel", 20))
    btn1 = tk.Button(gui, text="Accounts", width=30, command=accounts)
    btn2 = tk.Button(gui, text="Add Account", width=30, command=add_account)
    btn3 = tk.Button(gui, text="Exit", width=30, command=exit)

    label.pack()
    btn1.pack(pady=10)
    btn2.pack(pady=10)
    btn3.pack(pady=10)


def authenticate(password):
    """Checks entered password SHA-256 hex digest with saved master password SHA-256 hex digest"""
    hash_password = hashlib.sha512(password.encode()).hexdigest()
    with open("auth.key", "r") as key:
        key = key.read()
        if hash_password == key:
            pm.load_key_and_passwords()
            main_menu()
        else:
            label = tk.Label(gui, text="Invalid Password", bg="red", fg="black")
            label.pack()


def set_master_password():
    """Prompts for creation of master password"""
    label = tk.Label(gui, text="Set the Master Password", width=400, bg="lightblue", fg="black", font=("Ariel", 20))
    password = tk.Entry(gui, bg="lightgray", fg="black")
    submit_button = tk.Button(gui, text="Submit", command=lambda: pm.first_run(password.get()))

    label.pack(pady=20)
    password.pack(pady=10)
    submit_button.pack(pady=10)


def login_screen():
    """Displays a Login Screen"""
    label = tk.Label(gui, text="Enter Password", width=400, bg="lightblue", fg="black", font=("Ariel", 20))
    password = tk.Entry(gui, bg="lightgray", fg="black")
    submit_button = tk.Button(gui, text="Submit", command=lambda: authenticate(password.get()))

    label.pack(pady=20)
    password.pack(pady=10)
    submit_button.pack(pady=10)


def main():
    """Checks if this program has been executed before"""
    gui.geometry("400x300")
    gui.title("Password Manager")
    gui.config(bg="lightblue")

    if os.path.isfile("auth.key"):
        login_screen()
    else:
        set_master_password()

    gui.mainloop()


if __name__ == "__main__":
    main()
