# Secure FTP Server and Client

A secure FTP server and client application using FTPS (FTP over TLS) with file encryption using AES-128.

## Features

- **FTP over TLS (FTPS)**: Secure file transfer using encrypted connections.
- **AES-128 Encryption**: Files are encrypted before uploading and decrypted after downloading.
- **Graphical User Interface**: Both the client and server have a GUI for ease of use.

## Requirements

- Python 3.x
- Required Python packages:
  - pyftpdlib
  - tkinter

## Getting Started

### Server Setup

1. **Install Required Packages**:
    ```bash
    pip install pyftpdlib
    ```

2. **Generate TLS Certificates**:
    Generate a self-signed certificate and private key:
    ```bash
    openssl req -new -x509 -days 365 -nodes -out cert/cert.pem -keyout cert/key.pem
    ```

3. **Run the Server**:
    Save the server script as `server.py` and run:
    ```bash
    python server.py
    ```

### Client Setup

1. **Install Required Packages**:
    ```bash
    pip install tkinter
    ```

2. **Run the Client**:
    Save the client script as `client.py` and run:
    ```bash
    python client.py
    ```

## File Structure

- `server.py`: The FTP server script.
- `client.py`: The FTP client script.
- `AES128.py`: A module containing the AES-128 encryption and decryption functions.
- `cert/`: Directory containing the TLS certificate and key.
- `server_data/`: Directory where server files are stored.

## Usage

### Server

- The server starts automatically and listens for connections on port 2121.
- Server logs are displayed in the GUI.

### Client

- The client connects to the server and provides options to upload, download, and delete files.
- Files are encrypted before upload and decrypted after download using AES-128 encryption.

## Code Explanation

### Server (`server.py`)

The server uses `pyftpdlib` to handle FTP connections securely using TLS. It provides a GUI using `tkinter` to display logs and control the server.

#### Key Functions:
- `start_ftp_server()`: Starts the FTP server.
- `quit_server()`: Shuts down the server and exits the application.

### Client (`client.py`)

The client connects to the FTP server using FTPS and provides functionalities to upload, download, and delete files. It uses AES-128 for encrypting files before upload and decrypting them after download.

#### Key Functions:
- `encrypt_file(filepath)`: Encrypts the file at the given path using AES-128.
- `decrypt_file(encrypted_data)`: Decrypts the given data using AES-128.
- `upload_file()`: Encrypts and uploads the selected file to the server.
- `download_file()`: Downloads and decrypts the selected file from the server.
- `delete_file()`: Deletes the selected file from the server.
- `list_files()`: Lists all files on the server.
- `logout()`: Logs out from the server and exits the application.

## Acknowledgements

- [pyftpdlib](https://github.com/giampaolo/pyftpdlib) - A very complete and easy-to-use FTP server library.
- [tkinter](https://docs.python.org/3/library/tkinter.html) - The standard Python interface to the Tk GUI toolkit.
