
# Local Network File Server

**Full PC Browser Access with Auto-Generated Password and Secure Uploads**

This lightweight Python Flask app transforms your Windows PC into a local file server, allowing seamless browsing and file management over your LAN from any browser. Perfect for quick file sharing within trusted networks!

## Key Features
- **Full Filesystem Browsing**: Explore your PC's directories starting from a configurable `ROOT_DIR` (defaults to `C:\`).
- **Easy Downloads**: Click to download files from any browsable folder.
- **Safe Uploads**: Files are saved to a dedicated `uploads/` folder to bypass Windows permission issues.
- **Auto-Generated Password**: A new random admin password is created on every startup, stored in `.env`, and printed to the console for easy access.
- **Simple Login Protection**: A lightweight login screen secures access over the LAN.

⚠️ **Security Reminder**: This app is designed for **trusted local networks only**. Do **not** expose it to the public internet without additional security measures like hardened authentication, TLS, a reverse proxy, or VPN.

## Project Structure
```
local-network-file-server/
├── app.py                # Main Flask app (auto password generation)
├── run_waitress.py       # Optional: Run with Waitress for Windows
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md             # (This file)
├── templates/
│   ├── index.html
│   └── login.html
├── static/
│   └── style.css
└── uploads/              # Created at runtime (writable upload target)
```

## Quick Summary: What the App Does
1. **Startup Password Generation**: On launch, `app.py` creates a secure random password, saves it as `ADMIN_PASSWORD=<password>` in `.env` (appends if the file exists), and prints it to the console.
2. **Browsable UI**: Serves an interactive interface to list directories and files under `ROOT_DIR` (default: `C:\`).
3. **File Downloads**: Simply click a file to download it; navigate directories via URL paths.
4. **Secure Uploads**: Browser uploads are redirected to `ROOT_DIR/uploads/<current_path>` to avoid permission errors in protected folders.
5. **Session-Based Login**: Protects the UI with a password check against the generated value.

## Requirements
- **Operating System**: Windows (tested on Windows 10/11).
- **Python**: 3.8+ (3.11+ recommended).
- **Git**: Optional, for cloning the repo.

### Python Packages (from `requirements.txt`)
```
Flask>=2.2
waitress>=2.1
python-dotenv>=1.0
```

## Installation & Setup (Windows)
Open PowerShell and follow these steps:

```powershell
# Clone or copy the repo, then:
cd C:\path\to\local-file-server
python -m venv venv
# If PowerShell blocks scripts for venv activation, enable temporarily:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
# Activate venv (PowerShell):
.\venv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
```

## .env File
- Copy `.env.example` to `.env` to override defaults. The app will append `ADMIN_PASSWORD` on every start if needed.

Contents of `.env.example`:
```
# Copy to .env and edit values if you want to override defaults
FLASK_SECRET=changeme-please
PORT=8000
MAX_CONTENT_LENGTH=209715200
ROOT_DIR=C:\\
```

**Note**: The app uses `ROOT_DIR` from the environment if set; otherwise, it defaults to `C:\`.

## How the Auto-Password Works
- On every startup, a 12-character random password (letters, digits, punctuation) is generated and assigned to `ADMIN_PASSWORD`.
- If `.env` exists, it appends `ADMIN_PASSWORD=<new-password>` to ensure the latest is saved.
- The password is printed to the console, e.g.:
  ```
  New admin password generated: s%3R!aB7... (example)
  ```
- Use this to log in at `http://<your-pc-ip>:<port>`.

## Running the App
### Dev Server (Quick Test – Not for Production)
```powershell
python app.py
# Or explicitly (optional):
$env:FLASK_APP = "app.py"
flask run --host=0.0.0.0 --port=8000
```

### Recommended: Waitress for Multi-Client LAN Usage
```powershell
python run_waitress.py
```

Waitress provides a more robust server for Windows compared to Flask's built-in dev server.

## Windows Firewall Configuration
If devices on the LAN can't connect, allow the port through Firewall (run PowerShell as Administrator):

```powershell
New-NetFirewallRule -DisplayName "Allow Flask 8000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000 -Profile Private,Domain
```

## Accessing from Another Device on the LAN
1. Find your PC's IP:
   ```powershell
   ipconfig
   # Look for IPv4 Address under your active adapter
   ```

2. On another device (phone/laptop), open a browser and visit:
   ```
   http://<your-pc-ip>:8000
   ```
   You'll be prompted for the password from the console.

## Upload Behavior & Permissions
- To prevent `PermissionError` in protected folders (e.g., root `C:\`), uploads are saved to a dedicated `uploads/` folder within `ROOT_DIR`.
- **Example**: Uploading while browsing `C:\Users\You\Documents` saves to `C:\uploads\C\Users\You\Documents\` (created automatically). This keeps things organized and error-free.

## Security Notes (Read Carefully)
- This app is **not** designed for public exposure. For remote access, use a VPN (e.g., Tailscale, WireGuard), secure reverse proxy with TLS, and strong authentication.
- The `.env` file contains secrets – it's already in `.gitignore` by default.
- **Enhancements to Consider**: Hashed passwords, single-use tokens, IP allowlists, rate-limiting, and disabling listings for sensitive folders.

## Customization
- Change `ROOT_DIR` via `.env` or environment variable:
  ```powershell
  setx ROOT_DIR "D:\\some\folder"
  # Reopen terminal, then run python app.py
  ```
- Adjust `PORT`, `MAX_CONTENT_LENGTH`, or `FLASK_SECRET` in `.env`.

## Troubleshooting
- **No Output on Startup**: Ensure the correct file is run and venv is activated. Add a `print("Starting")` line for debugging.
- **PermissionError on Upload**: Handled by saving to `uploads/`; confirm the folder is writable.
- **Can't Access from Phone**: Verify same Wi-Fi network, check Firewall, and test with `Test-NetConnection -ComputerName <ip> -Port 8000`.

## Pushing to GitHub
`.env` is ignored by default. Before pushing:
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/local-file-server.git
git push -u origin main
```

## Next Steps / TODO
- Add hashed password storage instead of plain-text in `.env`.
- Optional: Implement HTTP Basic Auth and rate-limiting.
- Optional: Dockerfile for easier deployment.
- Optional: Add UI controls (rename, delete, create folder).

## License
This project is released under the MIT License. Add a `LICENSE` file if publishing.
```