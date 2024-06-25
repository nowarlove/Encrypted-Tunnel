from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
import os
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, END
import logging
from AES128 import encrypt_block, decrypt_block, key_expansion

SERVER_DATA_PATH = "server_data"
USERS_FILE = "users.txt"
AES_KEY = 'SEMOGAHOKILAHYAA'

class FileServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Management Service")
        self.root.geometry("500x400")

        self.create_widgets()
        self.load_users()

        self.key_schedule = key_expansion(AES_KEY)

        self.server_thread = threading.Thread(target=self.start_ftp_server, daemon=True)
        self.server_thread.start()

    def create_widgets(self):
        self.user_listbox = Listbox(self.root, width=60, height=15)
        self.user_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self.add_user_button = tk.Button(self.root, text="Add User", command=self.add_user)
        self.add_user_button.grid(row=1, column=0, padx=5, pady=5)

        self.delete_user_button = tk.Button(self.root, text="Delete User", command=self.delete_user)
        self.delete_user_button.grid(row=2, column=0, padx=5, pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_server)
        self.quit_button.grid(row=2, column=1, padx=5, pady=5)

    def load_users(self):
        self.users = {}
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as file:
                for line in file:
                    username, encrypted_password = line.strip().split(":")
                    self.users[username] = encrypted_password
        self.update_user_listbox()

    def save_users(self):
        with open(USERS_FILE, "w") as file:
            for username, encrypted_password in self.users.items():
                file.write(f"{username}:{encrypted_password}\n")

    def update_user_listbox(self):
        self.user_listbox.delete(0, END)
        for username in self.users:
            self.user_listbox.insert(END, username)

    def start_ftp_server(self):
        authorizer = DummyAuthorizer()
        for username, encrypted_password in self.users.items():
            password = self.decrypt_password(encrypted_password)
            authorizer.add_user(username, password, SERVER_DATA_PATH, perm="elradfmw")
        authorizer.add_anonymous(SERVER_DATA_PATH, perm="elradfmw")

        handler = TLS_FTPHandler
        handler.certfile = "cert/cert.pem"
        handler.keyfile = "cert/key.pem"
        handler.tls_control_required = True
        handler.tls_data_required = True
        handler.authorizer = authorizer

        handler.passive_ports = range(60000, 65535)

        address = ("", 2121)
        self.ftp_server = FTPServer(address, handler)
        self.ftp_server.serve_forever()

    def encrypt_password(self, password):
        password_bytes = [ord(char) for char in password.ljust(16, '\0')]
        encrypted_block = encrypt_block(password_bytes, self.key_schedule)
        return ''.join(f'{byte:02x}' for byte in encrypted_block)

    def decrypt_password(self, encrypted_password):
        encrypted_bytes = bytes.fromhex(encrypted_password)
        decrypted_block = decrypt_block(list(encrypted_bytes), self.key_schedule)
        return ''.join(chr(byte) for byte in decrypted_block).rstrip('\0')

    def add_user(self):
        username = simpledialog.askstring("Input", "Enter username:")
        if username in self.users:
            messagebox.showerror("Error", "User already exists")
            return
        password = simpledialog.askstring("Input", "Enter password:", show='*')
        encrypted_password = self.encrypt_password(password)
        self.users[username] = encrypted_password
        self.save_users()
        self.update_user_listbox()
        self.update_server_users()
        messagebox.showinfo("Success", "User added successfully")

    def delete_user(self):
        selected_user = self.user_listbox.get(tk.ACTIVE)
        if not selected_user:
            messagebox.showerror("Error", "No user selected")
            return
        del self.users[selected_user]
        self.save_users()
        self.update_user_listbox()
        self.update_server_users()
        messagebox.showinfo("Success", "User deleted successfully")

    def update_server_users(self):
        if hasattr(self, 'ftp_server'):
            self.ftp_server.close_all()
        self.server_thread = threading.Thread(target=self.start_ftp_server, daemon=True)
        self.server_thread.start()

    def quit_server(self):
        if hasattr(self, 'ftp_server'):
            self.ftp_server.close_all()
        self.root.quit()

def main():
    os.makedirs(SERVER_DATA_PATH, exist_ok=True)
    root = tk.Tk()
    app = FileServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
