import os as os
import utilities.Utilities as  utilities
import zipfile
import shutil as shutil
import nodestatus.NodeStatus as nodestatus

'''
Created on Sep 9, 2018

@author: Default
'''

def copyAllToMaster(nodeIP,sourcePath):
    
    backup_node_ip=nodestatus.getBackupNodeIp(nodeIP)
    sourcePathList1=sourcePath.split('/')
    sourcePathList2=sourcePathList1[len(sourcePathList1)-1].split('.')
    sourcePathFileName=sourcePathList2[0]
    if not os.path.isdir("../files/"+nodeIP):
        return [False,'ERROR CODE 2001: Home Directory for node :'+nodeIP+" doesn't exist"]
    elif not os.path.isfile(sourcePath):
        return [False,'ERROR CODE 2002: Invalid Source Path: :'+sourcePath]
    #elif not sourcePathFileName == nodeIP:
    #    return [False,"ERROR CODE 2003: Node IP address doesn't match with zip file name, Node IP:"+nodeIP+" , ZIP File Name:"+sourcePathFileName]
    else:
        
        utilities.createOrReplace("../temp/")
        shutil.move("../files/"+nodeIP+"/configClient.xml", "../temp/configClient.xml")

        shutil.rmtree("../files/" +nodeIP)
        #utilities.zipdir(sourcePath,"../temp")
        zip_ref = zipfile.ZipFile(sourcePath, 'r')
        zip_ref.extractall("../temp")
        zip_ref.close()       
        
        source1=sourcePath.split("/")
        source2=source1[len(source1)-1]
        source3=source2.split(".zip")[0]
        
        shutil.copytree("../temp/"+source3,"../files/"+nodeIP )

        
        shutil.move( "../temp/configClient.xml","../files/"+nodeIP+"/configClient.xml")
        
        
        utilities.createOrReplace("../temp/")
        shutil.move("../files/"+backup_node_ip+"/configClient.xml", "../temp/configClient.xml")

        shutil.rmtree("../files/" +backup_node_ip)
        #utilities.zipdir(sourcePath,"../temp")
        zip_ref = zipfile.ZipFile(sourcePath, 'r')
        zip_ref.extractall("../temp")
        zip_ref.close()       
        
        source1=sourcePath.split("/")
        source2=source1[len(source1)-1]
        source3=source2.split(".zip")[0]
        
        shutil.copytree("../temp/"+source3,"../files/"+backup_node_ip )

        
        shutil.move( "../temp/configClient.xml","../files/"+backup_node_ip+"/configClient.xml")        
 
        return True

#def copyChangesToMaster(src, dest):
    
    #for filename in os.listdir(src):

    #os.path.getmtime(path)

ret=copyAllToMaster('192.168.1.5','D://files.zip')
print(ret)
