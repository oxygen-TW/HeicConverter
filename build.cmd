pyinstaller -c -F installer.py
pyinstaller -c -F heic2jpg.py
mkdir dist\bin
copy dist\installer.exe dist\bin
copy dist\heic2jpg.exe dist\bin