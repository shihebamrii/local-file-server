# local-network-file-server

Lightweight Python app to serve files on your local network via a browser. No Python needed on client devices.

## Quick start (Windows)

1. Clone or copy this repo to your PC.
2. Open PowerShell in the project folder.

```powershell
# create venv and activate
python -m venv venv
# if you see script restrictions, run once in this window:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\\venv\\Scripts\\Activate.ps1

# install dependencies
pip install -r requirements.txt