@echo off

echo Building installer application...
pyinstaller installer/main.py --onefile --name "QuickConvert Installer" --icon "src/Icon.ico" --workpath "Temp" --distpath "build" --noconfirm --uac-admin
echo Installer application has been built!
pause