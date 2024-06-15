import ftplib
import tkinter as tk
from tkinter import filedialog, Listbox, END, SINGLE, messagebox
import os
from AES128 import encrypt_block, decrypt_block, key_expansion

FTP_HOST = "localhost"
FTP_PORT = 21
FTP_USER = "user"
FTP_PASS = "12345"
AES_KEY = 'SEMOGAHOKILAHYAA'

class FileClientApp:
    def __init__(self, root):
        self.ftp = ftplib.FTP()
        try:
            self.ftp.connect(FTP_HOST, FTP_PORT)
            self.ftp.login(FTP_USER, FTP_PASS)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error connecting to server: {e}")
            return

        self.root = root
        self.root.title("File Client")
        self.root.geometry("500x400")

        self.create_widgets()
        self.list_files()
        self.key_schedule = key_expansion(AES_KEY)

    def create_widgets(self):
        self.listbox = Listbox(self.root, selectmode=SINGLE, width=60, height=15)
        self.listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=1, column=0, padx=10, pady=10)

        self.download_button = tk.Button(self.root, text="Download File", command=self.download_file)
        self.download_button.grid(row=1, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete File", command=self.delete_file)
        self.delete_button.grid(row=1, column=2, padx=10, pady=10)

        self.list_button = tk.Button(self.root, text="List Files", command=self.list_files)
        self.list_button.grid(row=2, column=0, padx=10, pady=10)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.grid(row=2, column=2, pady=10)

    def encrypt_file(self, filepath):
        with open(filepath, "rb") as file:
            file_data = file.read()
        encrypted_data = []
        for i in range(0, len(file_data), 16):
            block = file_data[i:i+16]
            if len(block) < 16:
                block = block.ljust(16, b'\0')
            encrypted_data.extend(encrypt_block(list(block), self.key_schedule))
        return bytes(encrypted_data)

    def decrypt_file(self, encrypted_data):
        decrypted_data = []
        for i in range(0, len(encrypted_data), 16):
            block = encrypted_data[i:i+16]
            decrypted_data.extend(decrypt_block(list(block), self.key_schedule))
        return bytes(decrypted_data).rstrip(b'\0')

    def upload_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            try:
                encrypted_data = self.encrypt_file(filepath)
                with open(filepath, "wb") as file:
                    file.write(encrypted_data)
                with open(filepath, "rb") as file:
                    self.ftp.storbinary(f"STOR {filename}", file)
                messagebox.showinfo("Upload Success", f"File {filename} uploaded successfully")
                self.list_files()
                # Restore original file
                with open(filepath, "wb") as file:
                    file.write(self.decrypt_file(encrypted_data))
            except Exception as e:
                messagebox.showerror("Upload Error", f"Error uploading file {filepath}: {e}")

    def download_file(self):
        selected_file = self.listbox.get(tk.ACTIVE)
        if selected_file:
            save_path = filedialog.asksaveasfilename(initialfile=selected_file)
            if save_path:
                try:
                    with open(save_path, "wb") as file:
                        self.ftp.retrbinary(f"RETR {selected_file}", file.write)
                    with open(save_path, "rb") as file:
                        encrypted_data = file.read()
                    decrypted_data = self.decrypt_file(encrypted_data)
                    with open(save_path, "wb") as file:
                        file.write(decrypted_data)
                    messagebox.showinfo("Download Success", f"File {selected_file} downloaded successfully")
                except Exception as e:
                    messagebox.showerror("Download Error", f"Error downloading file {selected_file}: {e}")

    def delete_file(self):
        selected_file = self.listbox.get(tk.ACTIVE)
        if selected_file:
            try:
                self.ftp.delete(selected_file)
                messagebox.showinfo("Delete Success", f"File {selected_file} deleted successfully")
                self.list_files()
            except Exception as e:
                messagebox.showerror("Delete Error", f"Error deleting file {selected_file}: {e}")

    def list_files(self):
        try:
            self.listbox.delete(0, END)
            files = self.ftp.nlst()
            for file in files:
                self.listbox.insert(END, file)
        except Exception as e:
            messagebox.showerror("List Error", f"Error listing files: {e}")

    def logout(self):
        try:
            self.ftp.quit()
        except Exception as e:
            messagebox.showerror("Logout Error", f"Error logging out: {e}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileClientApp(root)
    root.mainloop()
