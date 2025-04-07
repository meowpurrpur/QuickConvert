@echo off

echo Building main application...
pyinstaller src/main.py --name "QuickConvert" --icon "src/Icon.ico" --workpath "Temp" --distpath "build" --add-data "src/Icon.ico;." --add-data "src/metal.json;." --noconfirm --noconsole
echo Main application has been built!
pause