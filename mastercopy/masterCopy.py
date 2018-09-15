import os as os
from utilities import  Utilities
import zipfile
import shutil as shutil
'''
Created on Sep 9, 2018

@author: Default
'''

def copyAllToMaster(nodeIP,sourcePath):
    sourcePathList1=sourcePath.split('/')
    sourcePathList2=sourcePathList1[len(sourcePathList1)-1].split('.')
    sourcePathFileName=sourcePathList2[0]
    if not os.path.isdir("../files/"+nodeIP):
        return [False,'ERROR CODE 2001: Home Directory for node :'+nodeIP+" doesn't exist"]
    elif not os.path.isfile(sourcePath):
        return [False,'ERROR CODE 2002: Invalid Source Path: :'+sourcePath]
    elif not sourcePathFileName == nodeIP:
        return [False,"ERROR CODE 2003: Node IP address doesn't match with zip file name, Node IP:"+nodeIP+" , ZIP File Name:"+sourcePathFileName]
    else:
        shutil.rmtree("../files/" +nodeIP)
        zip_ref = zipfile.ZipFile(sourcePath, 'r')
        zip_ref.extractall("../files")
        zip_ref.close()
        return True

#def copyChangesToMaster(src, dest):
    
    #for filename in os.listdir(src):

    #os.path.getmtime(path)

#ret=copyAllToMaster('12','../123.zip')
#print(ret)
