import json
import os

CONFIG_PATH = os.path.expanduser("~/.nightly_transfer_config.json")

def configure():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    else:
        config = {}

    config["smb_server"] = input(f"Enter SMB server (current: {config.get('smb_server', 'your.server.address')}): ") or config.get("smb_server", "your.server.address")
    config["share_name"] = input(f"Enter SMB share name (current: {config.get('share_name', 'share_name')}): ") or config.get("share_name", "share_name")
    config["username"] = input(f"Enter username (current: {config.get('username', 'your_username')}): ") or config.get("username", "your_username")
    config["password"] = input(f"Enter password (current: {config.get('password', 'your_password')}): ") or config.get("password", "your_password")
    config["remote_path"] = input(f"Enter remote path (current: {config.get('remote_path', '/path/to/central/folder')}): ") or config.get("remote_path", "/path/to/central/folder")
    config["local_folder"] = input(f"Enter local folder (current: {config.get('local_folder', '~/Downloads')}): ") or config.get("local_folder", "~/Downloads")
    config["schedule_time"] = input(f"Enter schedule time (current: {config.get('schedule_time', '01:00')}): ") or config.get("schedule_time", "01:00")

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    print("Configuration saved.")

if __name__ == "__main__":
    configure()
