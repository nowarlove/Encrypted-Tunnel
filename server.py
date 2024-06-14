import os
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

class FileServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Server")
        self.root.geometry("500x400")

        self.create_widgets()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.server.listen()
        self.log_server_info(f"[LISTENING] Server is listening on {IP}:{PORT}.")
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def create_widgets(self):
        self.server_info_area = tk.Text(self.root, width=60, height=5)
        self.server_info_area.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        self.server_info_area.config(state=tk.DISABLED)

        self.text_area = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_server)
        self.quit_button.grid(row=2, column=1, padx=10, pady=10)

    def log_server_info(self, message):
        self.server_info_area.config(state=tk.NORMAL)
        self.server_info_area.insert(tk.END, f"{message}\n")
        self.server_info_area.config(state=tk.DISABLED)
        self.server_info_area.see(tk.END)

    def log_message(self, message):
        self.text_area.insert(tk.END, f"{message}\n")
        self.text_area.see(tk.END)

    def update_file_list(self):
        files = os.listdir(SERVER_DATA_PATH)
        self.text_area.delete(1.0, tk.END)  # Delete everything in the text area
        self.text_area.insert(tk.END, "\n".join(files) + "\n" if files else "The server directory is empty\n")

    def accept_clients(self):
        while True:
            conn, addr = self.server.accept()
            self.log_server_info(f"[NEW CONNECTION] {addr} connected.")
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        conn.send("OK@Welcome to the File Server.".encode(FORMAT))

        while True:
            data = conn.recv(SIZE).decode(FORMAT)
            if not data:
                break
            cmd, *args = data.split("@")
            response = "OK@"

            if cmd == "LIST":
                files = os.listdir(SERVER_DATA_PATH)
                response += "\n".join(files) if files else "The server directory is empty"

            elif cmd == "UPLOAD":
                filename = args[0]
                filepath = os.path.join(SERVER_DATA_PATH, filename)
                with open(filepath, "wb") as f:
                    while True:
                        file_data = conn.recv(SIZE)
                        if file_data.endswith(b"<END>"):
                            f.write(file_data[:-5])
                            break
                        f.write(file_data)
                response += "File uploaded successfully."
                self.root.after(0, self.update_file_list)

            elif cmd == "DELETE":
                filename = args[0]
                filepath = os.path.join(SERVER_DATA_PATH, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    response += "File deleted successfully."
                else:
                    response += "File not found."
                self.root.after(0, self.update_file_list)

            conn.send(response.encode(FORMAT))

            if cmd == "LOGOUT":
                break

        conn.close()

    def quit_server(self):
        self.server.close()
        self.root.quit()

def main():
    os.makedirs(SERVER_DATA_PATH, exist_ok=True)
    root = tk.Tk()
    app = FileServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
