import os, time, requests

# Change this manually if your PC IP changes
url = "http://192.168.0.116:5000"

# Termux shared storage folders
fs = [
    "/data/data/com.termux/files/home/storage/shared/Pictures",
    "/data/data/com.termux/files/home/storage/shared/Documents",
]

# File that stores already uploaded file paths
uf = "uploaded.txt"

# Supported file types
ext = (
    ".jpg", ".jpeg", ".png", ".webp", ".heic",
    ".pdf", ".doc", ".docx", ".txt"
)


def load():
    if not os.path.exists(uf):
        return set()

    with open(uf, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save(p):
    with open(uf, "a") as f:
        f.write(p + "\n")


def ok(p):
    return p.lower().endswith(ext)


def send(p):
    try:
        with open(p, "rb") as f:
            files = {
                "file": (os.path.basename(p), f)
            }

            r = requests.post(url, files=files, timeout=10)

        if r.status_code == 200:
            print("Uploaded:", p)
            return True
        else:
            print("Failed:", p, r.status_code)
            return False

    except Exception as e:
        print("Error:", p)
        print(e)
        return False

def scan():
    up = load()

    for d in fs:
        if not os.path.exists(d):
            print("Folder not found:", d)
            continue

        for root, dirs, files in os.walk(d):
            for name in files:
                p = os.path.join(root, name)

                if p in up:
                    continue

                if not ok(p):
                    continue

                if send(p):
                    save(p)
                    up.add(p)


while True:
    scan()
    time.sleep(10)
