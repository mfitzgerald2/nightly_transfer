import os
import shutil
import socket
import json
from datetime import datetime
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open
import schedule
import time

# Default Configuration File Path
CONFIG_PATH = os.path.expanduser("~/.nightly_transfer_config.json")

# Load or Create Configuration
def load_config():
    default_config = {
        "smb_server": "your.server.address",
        "share_name": "share_name",
        "username": "your_username",
        "password": "your_password",
        "remote_path": "/path/to/central/folder",
        "local_folder": os.path.expanduser("~/Downloads"),
        "schedule_time": "01:00",
    }
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    else:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)

# SMB File Upload Function
def smb_upload_file(conn, session, tree, local_file, remote_folder):
    filename = os.path.basename(local_file)
    remote_file_path = os.path.join(remote_folder, filename)

    try:
        open_remote_file = Open(tree, remote_file_path, "r")
        open_remote_file.close()
        timestamp = datetime.now().strftime("_%Y%m%d")
        name, ext = os.path.splitext(filename)
        filename = f"{name}{timestamp}{ext}"
        remote_file_path = os.path.join(remote_folder, filename)
    except FileNotFoundError:
        pass

    with open(local_file, "rb") as f:
        remote_file = Open(tree, remote_file_path, "w")
        remote_file.write(f.read())
        remote_file.close()

def clean_up_local_files(local_files):
    for file in local_files:
        os.remove(file)

def nightly_transfer():
    config = load_config()
    smb_server = config["smb_server"]
    share_name = config["share_name"]
    username = config["username"]
    password = config["password"]
    remote_path = config["remote_path"]
    local_folder = config["local_folder"]

    hostname = socket.gethostname()
    destination_folder = os.path.join(remote_path, hostname)

    conn = Connection(uuid=None, server=smb_server, port=445)
    conn.connect()
    session = Session(conn, username=username, password=password)
    session.connect()
    tree = TreeConnect(session, share_name)
    tree.connect()

    try:
        open_remote_dir = Open(tree, destination_folder, "r")
        open_remote_dir.close()
    except FileNotFoundError:
        open_remote_dir = Open(tree, destination_folder, "w")
        open_remote_dir.close()

    files_to_transfer = [
        os.path.join(local_folder, file)
        for file in os.listdir(local_folder)
        if os.path.isfile(os.path.join(local_folder, file))
    ]

    for local_file in files_to_transfer:
        smb_upload_file(conn, session, tree, local_file, destination_folder)

    clean_up_local_files(files_to_transfer)

    tree.disconnect()
    session.disconnect()
    conn.disconnect()

if __name__ == "__main__":
    config = load_config()

    # Schedule the task at the configured time
    schedule.every().day.at(config["schedule_time"]).do(nightly_transfer)

    print("Scheduled to run at", config["schedule_time"], "every day.")
    while True:
        schedule.run_pending()
        time.sleep(1)