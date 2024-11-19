# Nightly File Transfer Script

This Python project automates the nightly transfer of files from a local folder (e.g., `Downloads`) to a central SMB file server. It supports configurable parameters and runs every night at a user-specified time.

---

## Features

- Cross-platform support (Windows, macOS, Linux)
- Configurable SMB server and folder paths
- Automatic scheduling using local time
- Resolves filename conflicts by appending the current date
- Basic UI for setting up configurations

---

## Requirements

- **Python**: Version 3.8 or higher  
- **Dependencies**: `smbprotocol`, `schedule`

Install the required dependencies with:

```bash
pip install smbprotocol schedule
```

---

## Setup

### Step 1: Configure the Script
Run the configuration UI to set up the script:

```bash
python config_ui.py
```

The script will prompt you for details such as the SMB server address, credentials, folder paths, and the scheduled time.

### Step 2: Run the Script
Once configured, you can execute the script with:

```bash
python nightly_transfer.py
```

The script will run in the background, waiting to execute at the scheduled time (default: `01:00 AM`).

---

## Building Executables

This repository is set up with **GitHub Actions** to create standalone executables for:

- **Windows**: `.exe` files
- **macOS**: `.app` files  

Built artifacts are available for download in the **Actions** tab of the repository after each workflow run.

---

## How It Works

1. **Transfer Files**:
   - Files from the configured local folder (e.g., `Downloads`) are copied to the central SMB server in a subfolder named after the computer’s hostname.
   - If a filename conflict exists, the script appends the current date to the filename.

2. **Scheduling**:
   - The script uses the `schedule` library to run the transfer process at the configured time (default: `01:00 AM`).

3. **Configuration File**:
   - The script saves its settings in a JSON file located at `~/.nightly_transfer_config.json`.  
   - You can edit this file directly or use the configuration UI to make changes.

---

## Repository Structure

- `nightly_transfer.py`: Main script that handles file transfers and scheduling.
- `config_ui.py`: Basic UI for setting up or modifying the configuration.
- `.github/workflows/build.yml`: GitHub Actions workflow for building `.exe` and `.app` files.