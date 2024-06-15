# FTP File Client and Server with AES-128 Encryption

## Overview
This project consists of an FTP server and client implemented in Python. The client can upload, download, and delete files on the server, with the added security feature of AES-128 encryption for file transfers. The server provides a graphical user interface (GUI) for monitoring and controlling the server.

## Features
- **FTP Server**: Uses `pyftpdlib` to provide an FTP server with user authentication and file permissions.
- **FTP Client**: Uses `ftplib` to connect to the FTP server and perform file operations.
- **AES-128 Encryption**: Implements AES-128 encryption for secure file transfers.

## Installation

1. Clone the repository:
   ```sh
   git clone [https://github.com/your-repository.git](https://github.com/putrisr22/Encrypted-Tunnel)
   cd your-repository
   ```

2. Install the required dependencies:
   ```sh
   pip install numpy pyftpdlib
   ```

## Usage

### Running the Server

1. Run the FTP server:
   ```sh
   python server.py
   ```

### Running the Client

1. Run the FTP client:
   ```sh
   python client.py
   ```

### AES-128 Encryption

The encryption and decryption are handled using `aes128.py`. The AES-128 implementation is custom-built and integrated into the client for securing file transfers.

## Code Explanation

### server.py

- **Dependencies**: `pyftpdlib`, `tkinter`, `threading`, `logging`
- **Functionality**:
  - Sets up an FTP server with user authentication and permissions.
  - Provides a GUI for monitoring server logs and controlling the server.

### client.py

- **Dependencies**: `ftplib`, `tkinter`, `os`, `aes128.py`
- **Functionality**:
  - Connects to the FTP server and provides options to upload, download, and delete files.
  - Uses AES-128 encryption for secure file transfers.

### aes128.py

- **Dependencies**: `numpy`
- **Functionality**:
  - Implements AES-128 encryption and decryption functions.
  - Provides methods for key expansion, block encryption, and block decryption.

## Example

### Encrypting and Uploading a File

1. Select a file to upload.
2. The file is encrypted using AES-128 before being sent to the server.
3. The encrypted file is uploaded to the server.

### Downloading and Decrypting a File

1. Select a file to download from the server.
2. The encrypted file is downloaded from the server.
3. The file is decrypted using AES-128 after being saved locally.

## Dependencies

- `numpy`: 1.26.4
- `pip`: 24.0
- `pyftpdlib`: 1.5.9
- `setuptools`: 65.5.0

## Troubleshooting

- Ensure that the FTP server is running before starting the client.
- Check the server logs for any errors related to file permissions or user authentication.
- Verify the encryption key and make sure it matches between the client and the server.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Contact

For any questions or issues, please contact [symbian071@gmail.com](mailto:symbian071@gmail.com).
