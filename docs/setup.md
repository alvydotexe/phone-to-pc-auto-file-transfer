# Setup Guide

This guide explains how to set up the Phone to PC Auto File Transfer project.

The project has two main parts:

1. **PC side** — Flask server receives uploaded files.
2. **Android phone side** — Termux Python script detects new files and uploads them to the PC.

## Requirements

### PC Requirements

- Linux / Fedora
- Python
- Flask
- Terminal
- systemd
- Git

### Android Requirements

- Termux
- Termux:Boot
- Python
- requests library
- Android storage permission

## Project Folder Structure

```text
phone-to-pc-auto-file-transfer/
│
├── server/
│   ├── app.py
│   └── templates/
│       └── form.html
│
├── phone/
│   └── uploader.py
│
├── systemd/
│   └── phone-server.service
│
├── docs/
│   ├── setup.md
│   └── workflow.md
│
├── .gitignore
├── README.md
└── LICENSE
```

# PC Setup

## 1. Install Python

Check Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

## 2. Install Flask

Install Flask:

```bash
pip install flask
```

or:

```bash
python -m pip install flask
```

## 3. Set Upload Folder

Inside the Flask server code, set the folder where uploaded files will be saved.

Example:

```python
UPLOAD_FOLDER = "/path/to/your/storage/folder"
```

Example for an HDD:

```python
UPLOAD_FOLDER = "/run/media/your-username/storage/phone"
```

Make sure the folder exists:

```bash
mkdir -p /path/to/your/storage/folder
```

## 4. Run the Flask Server

From the project folder, run:

```bash
python server/app.py
```

The server should run on:

```text
http://0.0.0.0:5000
```

This means the server is available on the local network.

# Manual IP Adjustment

This project uses the PC's local Wi-Fi IP address as the server address.

The PC IP address can change when:

- The router restarts
- The PC reconnects to Wi-Fi
- The PC connects to another Wi-Fi network
- The router assigns a new local IP address

Because of this, the server URL may need to be updated manually inside the wifi settings so that your pc ip address will be always be the same when you connect you home wifi.


## 1
. Quick Check

If files are not uploading, check these first:

- PC and phone are connected to the same Wi-Fi
- Flask server is running on the PC
- PC IP address is correct
- `SERVER_URL` in the phone script matches the current PC IP
- Port number is correct, usually `5000`

# Android Phone Setup

## 1. Install Termux

Install Termux on the Android phone.

Recommended source:

```text
F-Droid
```

## 2. Install Termux:Boot

Install Termux:Boot.

Termux:Boot is used to automatically start the uploader script after the phone restarts.

## 3. Give Termux Storage Access

Open Termux and run:

```bash
termux-setup-storage
```

Allow storage permission when Android asks.

After this, Termux can access shared phone storage.

# Important Termux Paths

Termux has its own Linux-like home directory.

The Termux home/root path is:

```text
/data/data/com.termux/files/home
```

This is where the uploader script usually lives.

Example:

```text
/data/data/com.termux/files/home/uploader.py
```

The shared Android storage path inside Termux is:

```text
/data/data/com.termux/files/home/storage/shared
```

## Watched Phone Folders

This project watches only two phone folders:

```text
/data/data/com.termux/files/home/storage/shared/Pictures
/data/data/com.termux/files/home/storage/shared/Documents
```

So the uploader script should use only these folders:

```python
FOLDERS = [
    "/data/data/com.termux/files/home/storage/shared/Pictures",
    "/data/data/com.termux/files/home/storage/shared/Documents",
]
```

If your phone uses a different folder name, update the path manually inside the script.

For example, some phones store camera photos in:

```text
/data/data/com.termux/files/home/storage/shared/DCIM
```

But for this project setup, only `Pictures` and `Documents` are used.

## 4. Install Python in Termux

Run:

```bash
pkg update
pkg install python
```

Check Python:

```bash
python --version
```

## 5. Install requests Library

Run:

```bash
pip install requests
```

The `requests` library is used to send files to the Flask server using HTTP POST.

## 6. Add the Phone Uploader Script

Place the phone uploader script inside Termux home.

Example location:

```text
/data/data/com.termux/files/home/uploader.py
```

If you are inside Termux home, create or edit it with:

```bash
nano uploader.py
```

## 7. Set the Server URL

Inside `uploader.py`, update the server URL:

```python
SERVER_URL = "http://YOUR_PC_IP:5000"
```

Example:

```python
SERVER_URL = "http://192.168.0.116:5000"
```

The IP address must be the PC's current local Wi-Fi IP address.

## 8. Run the Uploader Manually

Run:

```bash
python uploader.py
```

If everything is correct, new files from the selected phone folders will be uploaded to the PC.

# Termux:Boot Setup

Termux:Boot allows the phone uploader script to start automatically after the phone restarts.

## 1. Create Boot Folder

In Termux, run:

```bash
mkdir -p ~/.termux/boot
```

Full path:

```text
/data/data/com.termux/files/home/.termux/boot
```

## 2. Create Boot Script

Create a boot script:

```bash
nano ~/.termux/boot/start-uploader.sh
```

Add this:

```bash
#!/data/data/com.termux/files/usr/bin/bash

termux-wake-lock
cd /data/data/com.termux/files/home
python uploader.py
```

## 3. Make Boot Script Executable

Run:

```bash
chmod +x ~/.termux/boot/start-uploader.sh
```

## 4. Test the Boot Script Manually

Run:

```bash
~/.termux/boot/start-uploader.sh
```

If the uploader starts correctly, the boot script is working.

## 5. Restart the Phone

Restart the Android phone.

After restart:

1. Termux:Boot starts.
2. The boot script runs.
3. `uploader.py` starts automatically.
4. New files from `Pictures` and `Documents` are detected and uploaded.

# PC Auto Start With systemd

The Flask server can also start automatically when the PC boots.

## 1. Create systemd Service File

Example service file:

```text
systemd/phone-server.service
```

Example content:

```ini
[Unit]
Description=Phone File Upload Flask Server
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/phone-to-pc-auto-file-transfer
ExecStart=/usr/bin/python /path/to/phone-to-pc-auto-file-transfer/server/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Replace:

```text
your-username
/path/to/phone-to-pc-auto-file-transfer
```

with your real username and project path.

## 2. Copy Service File

```bash
sudo cp systemd/phone-server.service /etc/systemd/system/
```

## 3. Reload systemd

```bash
sudo systemctl daemon-reload
```

## 4. Enable Service

```bash
sudo systemctl enable phone-server.service
```

## 5. Start Service

```bash
sudo systemctl start phone-server.service
```

## 6. Check Service Status

```bash
sudo systemctl status phone-server.service
```

If it shows `active (running)`, the server is working.

# Testing the Full System

## 1. Start PC Server

```bash
sudo systemctl start phone-server.service
```

or manually:

```bash
python server/app.py
```

## 2. Check PC IP

```bash
hostname -I
```

## 3. Update Phone Script

Make sure the phone script has the correct server URL:

```python
SERVER_URL = "http://YOUR_PC_IP:5000"
```

Also make sure the watched folders are:

```python
FOLDERS = [
    "/data/data/com.termux/files/home/storage/shared/Pictures",
    "/data/data/com.termux/files/home/storage/shared/Documents",
]
```

## 4. Run Phone Script

```bash
python uploader.py
```

## 5. Add a New File on Phone

Add a new photo or document inside one of these folders:

```text
Pictures
Documents
```

The file should be sent to the PC automatically.

# Troubleshooting

## Files Are Not Uploading

Check:

- PC and phone are connected to the same Wi-Fi
- Flask server is running
- PC IP address is correct
- `SERVER_URL` is updated in the phone script
- Port `5000` is correct
- Termux has storage permission
- The file is inside `Pictures` or `Documents`
- The file type is supported by the uploader script

## Permission Issue in Termux

Run again:

```bash
termux-setup-storage
```

Then allow permission from Android settings if needed.

## Termux:Boot Not Starting Script

Check:

- Termux:Boot is installed
- Boot script exists in `~/.termux/boot`
- Boot script is executable
- Phone battery optimization is disabled for Termux and Termux:Boot

Make executable again:

```bash
chmod +x ~/.termux/boot/start-uploader.sh
```

## PC Server Not Starting on Boot

Check service status:

```bash
sudo systemctl status phone-server.service
```

Check logs:

```bash
journalctl -u phone-server.service
```

# Security Note

This setup is designed for local Wi-Fi only.

Do not expose the Flask server to the public internet without authentication, HTTPS, and proper security.
