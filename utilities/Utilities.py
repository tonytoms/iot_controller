import os as os
import shutil as shutil
import zipfile
'''
Created on Sep 9, 2018

@author: Default
'''

def createOrReplace(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
        
def zipdir(source, dest):
    shutil.make_archive(dest, 'zip', source)

def cutPasteFile(source,dest):
    shutil.move(source, dest)
def unzipWithoutRoot(source,dest):
    zip_ref = zipfile.ZipFile(source, 'r')
    zip_ref.extractall(dest)
    zip_ref.close()
    
    files = os.listdir(dest+"/"+source.split(".zip")[0])

    shutil.copytree(dest+"/"+source.split(".zip")[0],dest)

def checkExistOrCreate(path):
    if os.path.isdir(path):
        return True
    else:
        os.mkdir(path)
        return True
