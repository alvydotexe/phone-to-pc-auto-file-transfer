# Phone to PC Auto File Transfer

A local Wi-Fi based automation project that automatically transfers new photos, screenshots, and downloaded files from an Android phone to a PC.

The phone runs a Python script through Termux. The script detects new files, checks whether they were already uploaded, and sends them to a Flask server running on the PC. The PC receives the files and saves them directly to a selected storage folder such as an HDD.

## Why I Built This

I often had to clear my phone storage manually and search through old photos, screenshots, PDFs, and downloaded files whenever I needed them.

So I built this project to automatically back up new phone files to my PC whenever my phone and PC are connected to the same Wi-Fi network.

## Features

- Automatically detects new phone files
- Transfers files from Android to PC over local Wi-Fi
- Uses a Flask server on the PC
- Uses Termux on Android
- Starts automatically on Android boot using Termux:Boot
- Avoids duplicate file uploads
- Saves files directly to PC storage or HDD
- Starts the PC server automatically using systemd
- Uses manual PC IP setup when the local IP address changes
- Works without building a full Android app

## Apps and Tools Needed

### On PC

| App / Tool | Purpose |
|---|---|
| Linux / Fedora | Main operating system used for the PC server |
| Python | Runs the Flask server |
| Flask | Creates the local file upload server |
| Terminal | Used to run commands and manage the server |
| systemd | Starts the Flask server automatically on PC boot |
| Git | Tracks project files |
| GitHub | Hosts the project repository |
| VS Code / Any Code Editor | Used to edit the project files |

### On Android Phone

| App / Tool | Purpose |
|---|---|
| Termux | Runs the phone-side Python uploader script |
| Termux:Boot | Starts the uploader script automatically after phone restart |
| Python | Runs the uploader script |
| requests library | Sends files from phone to PC using HTTP POST |
| Android Storage Permission | Allows Termux to access photos, downloads, and screenshots |

## Tech Stack

- Python
- Flask
- Termux
- Termux:Boot
- HTTP POST requests
- Linux systemd
- Local Wi-Fi networking
- Git and GitHub

## Project Workflow

```text
Phone detects a new file
        ↓
Checks if the file was already uploaded
        ↓
Sends the file using an HTTP POST request
        ↓
Flask server receives the file
        ↓
PC saves the file to the selected storage folder
```

## Folder Structure

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
│   ├── workflow.md
│   └── setup.md
│
├── .gitignore
├── README.md
└── LICENSE
```

## PC Server Setup

Install Flask:

```bash
pip install flask
```

Run the Flask server:

```bash
python server/app.py
```

The server runs on:

```text
http://0.0.0.0:5000
```

From the phone, use the PC's local Wi-Fi IP address:

```text
http://YOUR_PC_IP:5000
```

Example:

```text
http://192.168.0.116:5000
```

## Android Phone Setup

Install Termux.

Give Termux storage access:

```bash
termux-setup-storage
```

Install Python:

```bash
pkg update
pkg install python
```

Install the requests library:

```bash
pip install requests
```

Update the server URL inside the phone uploader script:

```python
SERVER_URL = "http://YOUR_PC_IP:5000"
```

Run the uploader script:

```bash
python uploader.py
```

## Manual Server IP Setup

This project uses the PC's local Wi-Fi IP address as the server address.

The PC IP address can change when:

- The router restarts
- The PC reconnects to Wi-Fi
- The network assigns a new local IP
- The PC connects to a different Wi-Fi network

Because of this, the server URL may need to be updated manually inside the phone uploader script.

### Step 1: Find the PC IP Address

On the PC, run:

```bash
hostname -I
```

or:

```bash
ip addr
```

Look for an IP address like:

```text
192.168.0.xxx
```

Example:

```text
192.168.0.116
```

### Step 2: Update the Server URL on the Phone

Open the phone-side uploader script in Termux and update the `SERVER_URL` value:

```python
SERVER_URL = "http://YOUR_PC_IP:5000"
```

Example:

```python
SERVER_URL = "http://192.168.0.116:5000"
```

### Step 3: Restart the Phone Uploader Script

After changing the server URL, stop the old script and run it again:

```bash
python uploader.py
```

If the script is running automatically with Termux:Boot, restart the phone or manually restart the script from Termux.

### Important Note

The Flask server runs on the PC. So the server IP is the PC's local Wi-Fi IP address.

If the phone cannot send files, first check:

- PC and phone are connected to the same Wi-Fi
- Flask server is running on the PC
- The `SERVER_URL` in the phone script matches the PC's current IP
- The port number is correct, usually `5000`

## Auto Start on Android Boot

This project uses Termux:Boot to start the phone-side uploader script automatically after the phone restarts.

The boot script runs the Python uploader file from Termux.

Example flow:

```text
Phone restarts
        ↓
Termux:Boot starts
        ↓
Boot script runs
        ↓
Python uploader starts
        ↓
New files are detected and uploaded
```

## Auto Start on PC Boot

The Flask server can be started automatically using a systemd service.

Example service file is included here:

```text
systemd/phone-server.service
```

Copy the service file:

```bash
sudo cp systemd/phone-server.service /etc/systemd/system/
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable the service:

```bash
sudo systemctl enable phone-server.service
```

Start the service:

```bash
sudo systemctl start phone-server.service
```

Check the service status:

```bash
sudo systemctl status phone-server.service
```

## Problems I Solved

- Understanding how local servers work
- Sending files using HTTP POST requests
- Handling file uploads with Flask
- Giving Termux access to Android storage
- Avoiding duplicate file uploads
- Saving files directly to PC HDD
- Starting the Flask server automatically on PC boot
- Starting the phone uploader automatically with Termux:Boot
- Handling local IP address changes by manually updating the phone-side server URL
- Connecting Android and Linux over local Wi-Fi

## Future Improvements

- Add authentication
- Add upload history logs
- Add a web dashboard
- Add file type filters
- Organize uploaded files by date or file type
- Add automatic PC IP discovery
- Add clipboard sync between phone and PC
- Add notification after successful upload

## Security Note

This project is designed for local Wi-Fi use only.

Do not expose the Flask server directly to the public internet without proper authentication and security.

## Repository Description

```text
Automatically transfers new Android photos and downloads to a PC over local Wi-Fi using Termux, Termux:Boot, Python, and Flask.
```
