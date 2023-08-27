import tkinter as tk
from cryptography.fernet import Fernet
from tkinter import Tk


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
        main()

    def load_key(self, path):
        with open(str(path), 'rb') as f:
            self.key = f.read()
        main()

    def create_password_file(self, path):
        self.password_file = path
        with open(path, "w"):
            pass
        main()

    def load_password_file(self, path):
        self.password_file = path

        with open(self.password_file, 'r') as f:
            for line in f:
                site, encrypted_username, encrypted_password = line.split(":")
                self.password_dict[site] = [Fernet(self.key).decrypt(encrypted_username.encode()).decode(),
                                            Fernet(self.key).decrypt(encrypted_password.encode()).decode()]

        main()

    def add_password(self, site, username, password):
        self.password_dict[site] = [username, password]

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted_username = Fernet(self.key).encrypt(username.encode())
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted_username.decode() + ":" + encrypted_password.decode() + "\n")
        main()

    def get_password(self, site):
        display_password(site, self.password_dict[site][0],  self.password_dict[site][1])

    def delete_account(self, app):
        self.password_dict = {site: value for (site, value) in self.password_dict.items() if site != app}
        self.save_pass_dict()

    def modify_account(self, app, username, password):
        self.password_dict = {site: value for (site, value) in self.password_dict.items() if site != app}
        self.password_dict[app] = [username, password]
        self.save_pass_dict()

    def save_pass_dict(self):
        with open(self.password_file, 'w') as f:
            for key in self.password_dict:
                site = key
                username = self.password_dict[key][0]
                password = self.password_dict[key][1]
                encrypted_username = Fernet(self.key).encrypt(username.encode())
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted_username.decode() + ":" + encrypted_password.decode() + "\n")
        main()


class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x300")
        self.root.config(bg="white")
        self.root.title("Password Manager")

    def clearscreen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


def main_menu():
    gui.clearscreen()
    gui.root.config(bg="lightblue")
    label = tk.Label(gui.root, text="MAIN MENU", bg="gray", fg="black", font=("Ariel", 20), width=400)
    btn1 = tk.Button(gui.root, text="Create or Load Keys", command=create_load_key_menu, width=30)
    btn2 = tk.Button(gui.root, text="Create or load Password File", command=create_load_password_file, width=30)
    btn3 = tk.Button(gui.root, text="Add a password", command=add_password, width=30)
    btn4 = tk.Button(gui.root, text="Get a password", command=get_password, width=30)
    btn5 = tk.Button(gui.root, text="Quit", command=quit_app, width=30)

    label.pack()
    btn1.pack(pady=10)
    btn2.pack(pady=10)
    btn3.pack(pady=10)
    btn4.pack(pady=10)
    btn5.pack(pady=10)
    return


def create_load_key_menu():
    gui.clearscreen()
    label = tk.Label(gui.root, text="Create or Load Key", width=400, bg="gray", fg="black", font=("Ariel", 20))
    path_frame = tk.Frame(gui.root, bg="lightblue")
    path_label = tk.Label(path_frame, text="Enter a Filename / Path", bg="lightblue", fg="black")
    path = tk.Entry(path_frame, bg="lightgrey", fg="black")
    btn_frame = tk.Frame(gui.root, bg="lightblue")
    btn1 = tk.Button(btn_frame, text="Create Key", command=lambda: pm.create_key(path.get()))
    btn2 = tk.Button(btn_frame, text="Load Key", command=lambda: pm.load_key(path.get()))
    main_btn = tk.Button(gui.root, text="Return to Main Menu", command=main)

    label.pack()
    path_label.pack(side="left", padx=10)
    path.pack(side="right")
    path_frame.pack(pady=20)
    btn1.pack(side="left", padx=10)
    btn2.pack(side="right")
    btn_frame.pack()
    main_btn.pack(pady=70)


def create_load_password_file():
    gui.clearscreen()
    label = tk.Label(gui.root, text="Create or Load Password File", width=400, bg="gray", fg="black",
                     font=("Ariel", 20))
    path_frame = tk.Frame(gui.root, bg="lightblue")
    path_label = tk.Label(path_frame, text="Enter a Filename / Path", bg="lightblue", fg="black")
    path = tk.Entry(path_frame, bg="lightgrey", fg="black")
    btn_frame = tk.Frame(gui.root, bg="lightblue")
    btn1 = tk.Button(btn_frame, text="Create Password File", command=lambda: pm.create_password_file(path.get()))
    btn2 = tk.Button(btn_frame, text="Load Password File", command=lambda: pm.load_password_file(path.get()))
    main_btn = tk.Button(gui.root, text="Return to Main Menu", command=main)

    label.pack()
    path_label.pack(side="left")
    path.pack(side="right")
    path_frame.pack(pady=20)
    btn1.pack(side="left", padx=10)
    btn2.pack(side="right")
    btn_frame.pack()
    main_btn.pack(pady=60)


def add_password():
    gui.clearscreen()
    label = tk.Label(gui.root, text="Add Account", width=400, bg="gray", fg="black", font=("Ariel", 20))
    app_frame = tk.Frame(gui.root, bg="lightblue")
    app_label = tk.Label(app_frame, text="Enter the Application", bg="lightblue", fg="black", width=17)
    app = tk.Entry(app_frame, bg="lightgrey", fg="black", width=30)

    username_frame = tk.Frame(gui.root, bg="lightblue")
    username_label = tk.Label(username_frame, text="Enter the username", bg="lightblue", fg="black", width=17)
    username = tk.Entry(username_frame, bg="lightgrey", fg="black", width=30)

    password_frame = tk.Frame(gui.root, bg="lightblue")
    password_label = tk.Label(password_frame, text="Enter the password", bg="lightblue", fg="black", width=17)
    password = tk.Entry(password_frame, bg="lightgrey", fg="black", width=30)

    btn = tk.Button(gui.root, text="Submit", command=lambda: pm.add_password(app.get(), username.get(), password.get()))
    main_btn = tk.Button(gui.root, text="Return to Main Menu", command=main)

    label.pack()
    app_label.pack(side="left")
    app.pack(side="right")
    app_frame.pack(pady=15)
    username_label.pack(side="left")
    username.pack(side="right")
    username_frame.pack(pady=10)
    password_label.pack(side="left")
    password.pack(side="right")
    password_frame.pack()
    btn.pack(pady=30)
    main_btn.pack(pady=10)


def get_password():
    gui.clearscreen()
    label = tk.Label(gui.root, text="Get Password", width=400, bg="gray", fg="black", font=("Ariel", 20))
    label.pack()
    for key in pm.password_dict:
        btn = tk.Button(gui.root, text=key, width=30, command=lambda key1=key: pm.get_password(key1))
        btn.pack(pady=10)


def display_password(site, username, password):
    gui.clearscreen()
    label = tk.Label(gui.root, text=site, bg="gray", fg="black", width=400, font=("Ariel", 20))
    user_nm_frame = tk.Frame(gui.root, bg="lightblue")
    user_nm_label = tk.Label(user_nm_frame, text="Username: ", bg="lightblue", fg="black", width=17)
    user_nm = tk.Label(user_nm_frame, text=username, bg="lightgray", fg="black", width=30)
    passwd_frame = tk.Frame(gui.root, bg="lightblue")
    passwd_label = tk.Label(passwd_frame, text="Password: ", bg="lightblue", fg="black", width=17)
    passwd = tk.Label(passwd_frame, text=password, bg="lightgray", fg="black", width=30)
    main_btn = tk.Button(gui.root, text="Return to Main Menu", command=main)
    action_frame = tk.Frame(gui.root, background="lightblue")
    delete_btn = tk.Button(action_frame, text="Delete Account", command=lambda: pm.delete_account(site))
    modify_btn = tk.Button(action_frame, text="Modify Account", command=lambda: modify_account(site))

    label.pack()
    user_nm_label.pack(side="left")
    user_nm.pack(side="right")
    user_nm_frame.pack(pady=10)
    passwd_label.pack(side="left")
    passwd.pack(side="right")
    passwd_frame.pack(pady=5)
    delete_btn.pack(side="right", padx=5)
    modify_btn.pack(side="left")
    action_frame.pack(pady=10)
    main_btn.pack(pady=15)


def modify_account(site):
    gui.clearscreen()
    label = tk.Label(gui.root, text=site, font=("Ariel", 20))
    username_frame = tk.Frame(gui.root, bg="lightblue")
    username_label = tk.Label(username_frame, text="Enter the username", bg="lightblue", fg="black", width=17)
    username = tk.Entry(username_frame, bg="lightgrey", fg="black", width=30)

    password_frame = tk.Frame(gui.root, bg="lightblue")
    password_label = tk.Label(password_frame, text="Enter the password", bg="lightblue", fg="black", width=17)
    password = tk.Entry(password_frame, bg="lightgrey", fg="black", width=30)

    btn = tk.Button(gui.root, text="Submit", command=lambda: pm.modify_account(site, username.get(), password.get()))
    main_btn = tk.Button(gui.root, text="Return to Main Menu", command=main)

    label.pack()
    username_label.pack(side="left")
    username.pack(side="right")
    username_frame.pack(pady=10)
    password_label.pack(side="left")
    password.pack(side="right")
    password_frame.pack()
    btn.pack(pady=30)
    main_btn.pack(pady=10)


def quit_app():
    exit(0)


gui = GUI()
pm = PasswordManager()


def main():
    done = False
    if not done:
        main_menu()

    gui.root.mainloop()


if __name__ == "__main__":
    main()
