# https://imagemagick.org/script/download.php#windows

import os
from os import path
from os.path import isdir
from sys import exit
from wand.image import Image
from wand import exceptions
from ConvertImageEx import *

def GetFileExtension(path):
    return os.path.splitext(path)[1]


class ConvertImage():
    def __init__(self, setFormat) -> None:
        self.formatList = ["jpeg", "png", "bmp", "gif", "svg", "tiff"]

        if(setFormat not in self.formatList):
            raise FormatNotSupport

        self.format = setFormat
        self.defaultOutputDir = self.format.upper()

    def convertFile(self, inputFile, outputDir=None):
        if(not(os.path.isfile(inputFile))):
            raise ConvertImageFileNotFound

        if(outputDir != None and not(os.path.isdir(outputDir))):
            raise ConvertImageDirNotFound

        inputFileBaseName = os.path.basename(inputFile)
        inputFileDir = os.path.dirname(inputFile)

        if(outputDir == None):
            outputDir = os.path.join(inputFileDir, self.defaultOutputDir)
            outputFile = os.path.join(
                outputDir, inputFileBaseName + "." + self.format.lower())
        else:
            outputFile = os.path.join(
                outputDir, inputFileBaseName + "." + self.format.lower())

        if(not(os.path.isdir(outputDir))):
            os.mkdir(outputDir)
            print("目錄已建立：", outputDir)

        try:
            #print("I:", inputFile)
            with Image(filename=inputFile) as img:
                img.format = self.format
                print("Prossing:", inputFile)
                img.save(filename=outputFile)
        except exceptions.CorruptImageError:
            print("Abort:", inputFile)
            raise CanNotConvertImage

        return True

    def convertDir(self, inputDir, outputDir=None):
        if(not(os.path.isdir(inputDir))):
            raise ConvertImageDirNotFound

        if(outputDir != None and not(os.path.isdir(outputDir))):
            print(outputDir)
            raise ConvertImageDirNotFound

        fileList = os.listdir(inputDir)
        heicList = [x for x in fileList if GetFileExtension(
            x).upper() == ".HEIC"]

        # process
        for img in heicList:
            tmpOutputFile = outputDir
            # print(tmpOutputFile)
            if(tmpOutputFile != None and not(os.path.isdir(tmpOutputFile))):
                os.mkdir(tmpOutputFile)
            try:
                self.convertFile(os.path.join(inputDir, img), tmpOutputFile)
            except CanNotConvertImage:
                continue

    def convertRecursive(self, inputDir, outputDir=None):
        if(outputDir != None and not(os.path.isdir(outputDir))):
            raise ConvertImageDirNotFound

        if(not(os.path.isdir(inputDir))):
            raise ConvertImageDirNotFound

        for dirPath, dirNames, fileNames in os.walk(inputDir):
            for f in fileNames:
                if(GetFileExtension(f).upper() != ".HEIC"):
                    continue

                print(os.path.join(dirPath, f))
                try:
                    self.convertFile(os.path.join(dirPath, f), outputDir)
                except CanNotConvertImage:
                    continue
    @staticmethod
    def supportFormat():
        print(["jpeg", "png", "bmp", "gif", "svg", "tiff"])


if __name__ == "__main__":
    ci = ConvertImage()
    #ci.convertFile("test\\1.HEIC", "test")
    #ci.convertDir("test", "test\\jpegg")
    ci.convertRecursive("test", "test\\tttt")
