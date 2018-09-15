import os as os
import shutil as shutil

'''
Created on Sep 9, 2018

@author: Default
'''

def createOrReplace(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
        
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

    