import winreg
import os
import sys
import shutil 
import platform
import requests
import subprocess
from sys import exit

REG_PATH_BASE = "Directory\\Background\\shell"
REG_PATH_BASE2 = "Directory\\shell"
REG_PATH = "Directory\\Background\\shell\\ConvertHEIC"
REG_PATH_sub = "Directory\\Background\\shell\\ConvertHEIC\\command"
REG_PATH_dir1 = "Directory\\shell\\convertHEIC"
REG_PATH_dir2 = "Directory\\shell\\convertHEIC\\command"

def downloadImageWand():
    X64_URL = "https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.0.11-4-Q16-x64-dll.exe"
    X86_URL = "https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.0.11-4-Q16-x86-dll.exe"
    arch = platform.architecture()[0]

    #Download installer
    if(not(os.path.isfile("IW.exe"))):
        if(arch == "64bit"):
            print("Downloading MagicWand x64... Plz wait!")
            r = requests.get(X64_URL, stream=True, timeout=1800)
            with open("IW.exe", "wb+") as f:
                f.write(r.content)
        elif(arch == "32bit"):
                print("Downloading MagicWand x86... Plz wait!")
                r = requests.get(X86_URL, stream=True, timeout=1800)
                with open("IW.exe", "wb+") as f:
                    f.write(r.content)
    
    #開啟安裝程式
    print("Opening ImageWand installer...")
    process = subprocess.Popen("IW.exe", stdout=subprocess.PIPE, creationflags=0x08000000)
    process.wait()
    print("移除暫存檔..")
    os.remove("IW.exe")
    print("IW.exe has been removed.")

def install(exePath):
    workCMD = exePath + " -d \"%V\""
    workCMD_dir = exePath + " -d %L"
    print(REG_PATH)
    try:
        #Reg1
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, REG_PATH)
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, REG_PATH_sub)
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, REG_PATH_sub, 0,
                                      (winreg.KEY_WRITE + winreg.KEY_WOW64_64KEY))
        winreg.SetValueEx(registry_key, "", 0, winreg.REG_SZ, workCMD)
        winreg.CloseKey(registry_key)

        #Reg2
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, REG_PATH_dir1)
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, REG_PATH_dir2)
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, REG_PATH_dir2, 0,
                                      (winreg.KEY_WRITE + winreg.KEY_WOW64_64KEY))
        winreg.SetValueEx(registry_key, "", 0, winreg.REG_SZ, workCMD_dir)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError as e:
        print(e)
        return False


def uninstall():
    try:
        #Reg 1
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,REG_PATH_BASE,access=winreg.KEY_WRITE) as reg:
            winreg.DeleteKey(reg, "ConvertHEIC\\command")
            winreg.DeleteKey(reg, "ConvertHEIC")

        #Reg 2
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,REG_PATH_BASE2,access=winreg.KEY_WRITE) as reg:
            winreg.DeleteKey(reg, "ConvertHEIC\\command")
            winreg.DeleteKey(reg, "ConvertHEIC")

    except FileNotFoundError as e:
        print(e)
        return False 
    return True

def main():
    EXE_PATH = os.path.join(os.getenv("systemdrive"), os.path.join(os.getenv('HOMEPATH'), "heic2jpg") )
    EXE_ORI_PATH = "bin/heic2jpg.exe"
    Installer_ORI_PATH = "bin/install.exe"
    Installer_DEST_PATH = os.path.join(EXE_PATH, "install.exe")
    EXE_NAME = "heic2jpg.exe"

    if(len(sys.argv) != 2):
        print("參數錯誤[install | uninstall]")
        exit(1)
    
    if(sys.argv[1].lower() not in ["install", "uninstall"]):
        print("參數錯誤[install | uninstall]")
        exit(1)

    if(sys.argv[1].lower() == "install"):
        downloadImageWand()
        try:
            if(os.path.isdir(EXE_PATH)):
                print("目錄已存在", EXE_PATH)
            else:
                os.mkdir(EXE_PATH)
                print("Create Dir", EXE_PATH)
            Dest_EXE_path = os.path.join(EXE_PATH, EXE_NAME)
            shutil.copyfile(EXE_ORI_PATH, Dest_EXE_path)
            print("Copy file: installer",  Installer_DEST_PATH)
            shutil.copyfile(Installer_ORI_PATH, Installer_DEST_PATH)
            print("Copy file: heic2jpg",  Dest_EXE_path)
            #input("Do you want to write command to register?")
            print("EXE REG PATH", Dest_EXE_path)
            install(Dest_EXE_path)
            print("Install finished!")
        except Exception as e:
            print("Install Error:", e)
    
    elif(sys.argv[1].lower() == "uninstall"):
        if(not(os.path.isdir(EXE_PATH))):
            print("未發現安裝目錄")
            exit(1)
        shutil.rmtree(EXE_PATH, ignore_errors=True)
        print("Remove", EXE_PATH)
        uninstall()
        print("Uninstall register")

if __name__ == "__main__":
    if(sys.platform != "win32"):
        print("Installer support Windows system only!")
        exit(1)
    main()