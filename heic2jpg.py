import os
import argparse
import platform
from sys import exit
from convert import *

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-d", "--directory", dest="dirPath", help="The input directory.")
group.add_argument("-f", "--file", dest="filename", help="The input fingle file.")

parser.add_argument("-o", "--output", help="The output directory.",
                    dest="outputDir")
parser.add_argument("-r", "--recursive", help="Use recursive mode",
                    action="store_true")

parser.add_argument("-t", "--type", help="Output image type.",
                    dest="outputFormat")

args = parser.parse_args()

# 處理參數
outputDir = args.outputDir
isRecursive = args.recursive
outputFormat = args.outputFormat

if(outputFormat == None):
    outputFormat = "jpeg"

try:
    ci = ConvertImage(outputFormat)
    print("輸出格式：", outputFormat)
except FormatNotSupport:
    print("Support format:")
    ConvertImage.supportFormat()
    exit(1)

if(args.dirPath != None):
    try:
        if(args.recursive):
            print("recursive mode on")
            ci.convertRecursive(args.dirPath, outputDir)
        else:
            ci.convertDir(args.dirPath, outputDir)
    except ConvertImageDirNotFound:
        print("Err:", args.dirPath)
        print("找不到路徑或無效路徑")
    except CanNotConvertImage:
        print("無法轉換檔案")
        
elif(args.filename != None):
    try:
        ci.convertFile(args.filename, outputDir)    
    except CanNotConvertImage:
        print("無法轉換檔案")
    except ConvertImageFileNotFound:
        print("Err:", args.filename)
        print("找不到檔案")

print("All done!")
input("輸入任意鍵繼續")


