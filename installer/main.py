import subprocess
import sys, os
import requests
import zipfile
from tqdm import tqdm
import winreg

def IsChocolateyInstalled():
    try:
        subprocess.run(['choco', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def InstallChocolatey():
    try:
        subprocess.run(['powershell', '-Command', 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))'], check=True)
        
        os.system("cls")
        print("Chocolatey has been installed successfully! Please restart the installer.")
        os.system("pause")
        sys.exit(-1)

    except subprocess.CalledProcessError:
        print("Failed to install Chocolatey. Please install it manually.")
        sys.exit(1)

def InstallFFmpeg():
    if not IsChocolateyInstalled():
        print("Chocolatey is not installed. Installing Chocolatey first.")
        InstallChocolatey()
    
    try:
        subprocess.run(['choco', 'install', 'ffmpeg', '-y'], check=True)

        os.system("cls")
        print("FFmpeg has been installed successfully! Please restart the installer.")
        os.system("pause")
        sys.exit(-1)
    except subprocess.CalledProcessError:
        print("Failed to install FFmpeg. Please ensure you have Chocolatey installed and try again.")
    except FileNotFoundError:
        print("Chocolatey is not installed. Please install Chocolatey first.")
        sys.exit(1)

def IsFFmpegInstalled():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    
def AddContextMenuItem(MenuName, Command, IconPath):
    try:
        KeyPath = f"*\\shell\\{MenuName}"
        Key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, KeyPath)
        winreg.SetValueEx(Key, "Icon", 0, winreg.REG_SZ, IconPath)
        CommandKey = winreg.CreateKey(Key, "command")
        winreg.SetValueEx(CommandKey, "", 0, winreg.REG_SZ, Command)
    finally:
        winreg.CloseKey(Key)
        winreg.CloseKey(CommandKey)
    
if not IsFFmpegInstalled():
    print("Installing FFmpeg, please wait...")
    InstallFFmpeg()

print("Downloading latest version...")
ApiUrl = f'https://api.github.com/repos/meowpurrpur/QuickConvert/releases/latest'
Response = requests.get(ApiUrl)
ReleaseData = Response.json()

AssetUrl = None
for Asset in ReleaseData['assets']:
    if 'QuickConvert.zip' in Asset['name']:
        AssetUrl = Asset['browser_download_url']
        break

if not AssetUrl:
    print("QuickConvert.zip not found in release assets.")
    sys.exit(1)

Response = requests.get(AssetUrl, stream=True)
ProgramDataPath = os.path.join(os.getenv('ProgramData'), 'QuickConvert')
if not os.path.exists(ProgramDataPath):
    os.makedirs(ProgramDataPath)

ZipFilePath = os.path.join(ProgramDataPath, 'QuickConvert.zip')
TotalSize = int(Response.headers.get('content-length', 0))

with open(ZipFilePath, 'wb') as File, tqdm(total=TotalSize, unit='B', unit_scale=True) as Bar:
    for Data in Response.iter_content(chunk_size=1024):
        if Data:
            File.write(Data)
            Bar.update(len(Data))

with zipfile.ZipFile(ZipFilePath, 'r') as ZipRef:
    ZipRef.extractall(ProgramDataPath)

os.remove(ZipFilePath)

print("Downloaded latest version! Setting up context menu entry...")
AddContextMenuItem("QuickConvert", f'{os.path.join(ProgramDataPath, "QuickConvert.exe")} "%1"', os.path.join(ProgramDataPath, "_internal/Icon.ico"))

print("Installation done! Press enter to exit...")
os.system("pause")
sys.exit(0)