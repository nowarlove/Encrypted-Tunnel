from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
import os
import threading
import tkinter as tk
from tkinter import scrolledtext
import logging
from logging.handlers import QueueHandler, QueueListener
import queue

SERVER_DATA_PATH = "server_data"

class TkinterLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record)
        self.text_widget.after(0, self.text_widget.insert, tk.END, log_entry + '\n')
        self.text_widget.after(0, self.text_widget.see, tk.END)

class FileServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Server")
        self.root.geometry("500x400")

        self.create_widgets()
        self.setup_logging()

        self.server_thread = threading.Thread(target=self.start_ftp_server, daemon=True)
        self.server_thread.start()

    def create_widgets(self):
        self.server_info_area = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.server_info_area.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        self.server_info_area.config(state=tk.NORMAL)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_server)
        self.quit_button.grid(row=1, column=1, padx=10, pady=5)

    def setup_logging(self):
        log_queue = queue.Queue()
        queue_handler = QueueHandler(log_queue)
        queue_listener = QueueListener(log_queue, TkinterLogHandler(self.server_info_area))
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.addHandler(queue_handler)
        queue_listener.start()

    def start_ftp_server(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user("user", "12345", SERVER_DATA_PATH, perm="elradfmw")
        authorizer.add_anonymous(SERVER_DATA_PATH, perm="elradfmw")

        handler = TLS_FTPHandler
        handler.certfile = "cert/cert.pem"
        handler.keyfile = "cert/key.pem"
        handler.tls_control_required = True
        handler.tls_data_required = True
        handler.authorizer = authorizer

        handler.passive_ports = range(60000, 65535)  # Menetapkan kisaran port pasif

        address = ("", 2121)
        self.ftp_server = FTPServer(address, handler)
        logging.info("[STARTING] FTP server is starting.")
        self.ftp_server.serve_forever()

    def quit_server(self):
        self.ftp_server.close_all()
        self.root.quit()

def main():
    os.makedirs(SERVER_DATA_PATH, exist_ok=True)
    root = tk.Tk()
    app = FileServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
