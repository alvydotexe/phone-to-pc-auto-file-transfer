# Project Workflow

This document explains how the Phone to PC Auto File Transfer system works.

The project has two main parts:

1. **PC server**
2. **Android phone uploader**

## High-Level Workflow

```text
Android phone detects new files
        ↓
Phone checks if the file was already uploaded
        ↓
Phone sends the file to the PC using HTTP POST
        ↓
Flask server receives the file
        ↓
PC saves the file to the selected storage folder
```

## PC Side Workflow

The PC runs a Flask server.

### Step 1: Start Flask Server

The Flask server starts on the PC using:

```bash
python app.py
```

Or automatically using systemd.

The server runs on:

```text
0.0.0.0:5000
```

This allows other devices on the same Wi-Fi network to access the server using the PC's local IP address.

Example:

```text
http://192.168.0.116:5000
```

### Step 2: Wait for File Upload

The Flask server waits for a file sent through a POST request.

The upload field name is:

```text
file
```

### Step 3: Save File

When the PC receives a file, it saves the file inside the selected upload folder.

Example folder:

```text
/run/media/alvy/storage/phone
```

## Android Phone Side Workflow

The phone runs a Python script using Termux.

### Step 1: Scan Selected Folders

The uploader script scans these folders:

```text
/data/data/com.termux/files/home/storage/shared/Pictures
/data/data/com.termux/files/home/storage/shared/Documents
```

These folders contain photos and documents from the phone.

### Step 2: Check File Type

The script checks if the file type is supported.

Example supported file types:

```text
.jpg
.jpeg
.png
.webp
.heic
.pdf
.doc
.docx
.txt
```

### Step 3: Check Duplicate Uploads

The script uses:

```text
uploaded.txt
```

This file stores the paths of files that were already uploaded.

If a file path already exists in `uploaded.txt`, the script skips it.

This prevents uploading the same file again and again.

### Step 4: Send File to PC

If the file is new, the phone sends it to the Flask server using an HTTP POST request.

The server URL is set manually inside the uploader script.

Example:

```python
url = "http://192.168.0.116:5000"
```

If the PC IP changes, this URL must be updated manually.

### Step 5: Save Upload Record

If the upload succeeds, the file path is saved in:

```text
uploaded.txt
```

After that, the script will not upload the same file again.

## Auto Start Workflow

## PC Auto Start

The PC server can start automatically using systemd.

Workflow:

```text
PC boots
        ↓
systemd starts phone-server.service
        ↓
Flask server starts
        ↓
PC waits for uploads
```

## Phone Auto Start

The phone uploader can start automatically using Termux:Boot.

Workflow:

```text
Phone restarts
        ↓
Termux:Boot runs boot script
        ↓
Boot script starts uploader.py
        ↓
Uploader scans Pictures and Documents
        ↓
New files are uploaded to PC
```

## Manual IP Workflow

The PC local IP address can change.

This can happen when:

- Router restarts
- PC reconnects to Wi-Fi
- PC connects to a different network
- Router assigns a new local IP

When this happens:

```text
Find new PC IP
        ↓
Open uploader.py in Termux
        ↓
Update url variable
        ↓
Restart uploader.py
```

Example:

```python
url = "http://YOUR_PC_IP:5000"
```

## Full System Flow

```text
PC starts
        ↓
systemd starts Flask server
        ↓
Phone starts
        ↓
Termux:Boot starts uploader.py
        ↓
Uploader scans Pictures and Documents
        ↓
Uploader checks uploaded.txt
        ↓
New file found
        ↓
File sent to Flask server
        ↓
Flask server saves file to PC storage
        ↓
File path saved in uploaded.txt
        ↓
Uploader waits and scans again
```

## Current Limitations

- PC IP must be updated manually if it changes
- Phone and PC must be connected to the same Wi-Fi
- No authentication is added yet
- The server is designed for local network use only

## Future Workflow Improvements

- Automatic PC IP discovery
- Upload history dashboard
- File organization by date or type
- Authentication for safer uploads
- Clipboard sync between phone and PC
