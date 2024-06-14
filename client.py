import socket
import tkinter as tk
from tkinter import filedialog, Listbox, END, SINGLE, messagebox
import threading
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 4096

class FileClientApp:
    def __init__(self, root):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(ADDR)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error connecting to server: {e}")
            return

        self.root = root
        self.root.title("File Client")
        self.root.geometry("500x400")

        self.create_widgets()
        self.listen_to_server()

    def create_widgets(self):
        self.listbox = Listbox(self.root, selectmode=SINGLE, width=60, height=15)
        self.listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=1, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete File", command=self.delete_file)
        self.delete_button.grid(row=1, column=2, padx=10, pady=10)

        self.list_button = tk.Button(self.root, text="List Files", command=self.list_files)
        self.list_button.grid(row=2, column=0, padx=10, pady=10)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.grid(row=2, column=2, pady=10)

    def send_command(self, command):
        try:
            self.client.send(command.encode(FORMAT))
        except Exception as e:
            messagebox.showerror("Command Error", f"Error sending command {command}: {e}")

    def upload_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            self.send_command(f"UPLOAD@{filename}")
            threading.Thread(target=self._upload_file_thread, args=(filepath,)).start()

    def _upload_file_thread(self, filepath):
        try:
            with open(filepath, "rb") as f:
                while file_data := f.read(SIZE):
                    self.client.send(file_data)
                self.client.send(b"<END>")
        except Exception as e:
            messagebox.showerror("Upload Error", f"Error uploading file {filepath}: {e}")

    def delete_file(self):
        selected_file = self.listbox.get(tk.ACTIVE)
        if selected_file:
            self.send_command(f"DELETE@{selected_file}")

    def list_files(self):
        self.send_command("LIST")

    def logout(self):
        self.send_command("LOGOUT")
        self.client.close()
        self.root.destroy()

    def listen_to_server(self):
        def listen():
            while True:
                try:
                    data = self.client.recv(SIZE)
                    if not data:
                        break

                    parts = data.split(b'@', 1)
                    cmd = parts[0].decode(FORMAT)
                    msg = parts[1].decode(FORMAT) if len(parts) > 1 else ""

                    if cmd == "DISCONNECTED":
                        break
                    elif cmd == "OK":
                        self.listbox.delete(0, END)
                        files = msg.split("\n")
                        for file in files:
                            if file:
                                self.listbox.insert(END, file)
                except Exception as e:
                    messagebox.showerror("Server Error", f"Error receiving data: {e}")
                    break

        threading.Thread(target=listen, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileClientApp(root)
    root.mainloop()
