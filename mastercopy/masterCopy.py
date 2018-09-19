'''
Created on Sep 12, 2018

@author: Tony Toms

-------------Desc:----------------------

This class is the master copier.
This class copies the files to the master controller
This class Create all config files

----------------main variables--------------
# ret_status-  this list has all the informations regarding the running of each method. this variable is returned to the controller at the end
            ret_status[0] - True if task completed and false if an issue occurred
--------------------------------------
'''


import os as os
import utilities.Utilities as  utilities
import zipfile
import shutil as shutil
import nodestatus.NodeStatus as nodestatus
import sys
import traceback


#This function copies all the files from sourcePath Zip to node folders
def copyAllToMaster(nodeIP,sourcePath):


    ret_status=[True,"Step 1(of 18) - Check config files","Step 2(of 18) - Check Directory for node","Step 3(of 18) - Check directory for backup node","Step 4(of 18) - check Home directory "
                ,"Step 5(of 18) - Create Temp Folder","Step 6(of 18) - Copy Main Node config to temp ","Step 7(of 18) - Truncate Node Directory "
                ,"Step 8(of 18) -Extract Node Files to Temp ","Step 9(of 18) - Get Zip File Name","Step 10(of 18) - Copy node files from temp to node directory"
                ,"Step 11(of 18) - Copy node Config file to node Directory"
                
                ,"Step 12(of 18) - Create Temp Folder","Step 13(of 18) - Copy Backup Node config to temp ","Step 14(of 18) - Truncate Backup Node Directory "
                ,"Step 15(of 18) -Extract Backup Node Files to Temp ","Step 16(of 18) - Get Zip File Name","Step 17(of 18) - Copy Backup node files from temp to node directory"
                ,"Step 18(of 18) - Copy Backup node Config file to backup node Directory"]
    print("\n Running startBackupNodeExecution() \n")        
    
    try:
                
        backup_node_ip=nodestatus.getBackupNodeIp(nodeIP)
        if( backup_node_ip==""):
            ret_status[0]=False
            ret_status.append('ERROR CODE 2002: No Backup Node Ip found for Node IP :'+nodeIP)
            return ret_status  
        ret_status[1]=ret_status[1]+" :Done"          
        sourcePathList1=sourcePath.split(os.sep)
        sourcePathList2=sourcePathList1[len(sourcePathList1)-1].split('.')
        sourcePathFileName=sourcePathList2[0]
        if not os.path.isdir(".."+os.sep+"files"+os.sep+nodeIP):
            ret_status[0]=False
            ret_status.append('ERROR CODE 2001: Home Directory for node :'+nodeIP+" doesn't exist")
            return ret_status
        elif not os.path.isdir(".."+os.sep+"files"+os.sep+backup_node_ip):
            ret_status[0]=False
            ret_status[2]=ret_status[2]+" : Done"
            ret_status.append('ERROR CODE 2001: Home Directory for backup node :'+nodeIP+" doesn't exist")
            return ret_status
        elif not os.path.isfile(sourcePath):
            ret_status[0]=False
            ret_status[2]=ret_status[2]+" : Done"
            ret_status[3]=ret_status[3]+" : Done"
            ret_status.append('ERROR CODE 2002: Invalid Source Path: :'+sourcePath)
            return ret_status

        else:
            ret_status[2]=ret_status[2]+" : Done"
            ret_status[3]=ret_status[3]+" : Done"            
            ret_status[4]=ret_status[4]+" : Done"            
            
            ##########  Managing Main Node Copies ##########################
            utilities.createOrReplace(".."+os.sep+"temp"+os.sep)
            ret_status[5]=ret_status[5]+" : Done"
            
            shutil.move(".."+os.sep+"files"+os.sep+nodeIP+os.sep+"configClient.xml", ".."+os.sep+"temp"+os.sep+"configClient.xml")
            ret_status[6]=ret_status[6]+" : Done"
    
            shutil.rmtree(".."+os.sep+"files"+os.sep +nodeIP)
            ret_status[7]=ret_status[7]+" : Done"
            
            zip_ref = zipfile.ZipFile(sourcePath, 'r')
            zip_ref.extractall(".."+os.sep+"temp")
            zip_ref.close() 
            ret_status[8]=ret_status[8]+" : Done"      
            
            source1=sourcePath.split(os.sep)
            source2=source1[len(source1)-1]
            source3=source2.split(".zip")[0]
            ret_status[9]=ret_status[9]+" : Done"
            
            
            shutil.copytree(".."+os.sep+"temp"+os.sep+source3,".."+os.sep+"files"+os.sep+nodeIP )
            ret_status[10]=ret_status[10]+" : Done"
            
            shutil.move( ".."+os.sep+"temp"+os.sep+"configClient.xml",".."+os.sep+"files"+os.sep+nodeIP+os.sep+"configClient.xml")
            ret_status[11]=ret_status[11]+" : Done"
            
            
            ##########  Managing Backup Node Copies ##########################
            
            
            
            utilities.createOrReplace(".."+os.sep+"temp"+os.sep)
            ret_status[12]=ret_status[12]+" : Done"
            
            shutil.move(".."+os.sep+"files"+os.sep+backup_node_ip+os.sep+"configClient.xml", ".."+os.sep+"temp"+os.sep+"configClient.xml")
            ret_status[13]=ret_status[13]+" : Done"
    
            shutil.rmtree(".."+os.sep+"files"+os.sep +backup_node_ip)
            ret_status[14]=ret_status[14]+" : Done"
            
            #utilities.zipdir(sourcePath,"../temp")
            zip_ref = zipfile.ZipFile(sourcePath, 'r')
            zip_ref.extractall(".."+os.sep+"temp")
            zip_ref.close()
            ret_status[15]=ret_status[15]+" : Done"       
            
            source1=sourcePath.split(os.sep)
            source2=source1[len(source1)-1]
            source3=source2.split(".zip")[0]
            ret_status[16]=ret_status[16]+" : Done"
            
            shutil.copytree(".."+os.sep+"temp"+os.sep+source3,".."+os.sep+"files"+os.sep+backup_node_ip )
            ret_status[17]=ret_status[17]+" : Done"
            
            shutil.move( ".."+os.sep+"temp"+os.sep+"configClient.xml",".."+os.sep+"files"+os.sep+backup_node_ip+os.sep+"configClient.xml")  
            ret_status[18]=ret_status[18]+" : Done"      
     
    except:
        ret_status[0]=False
        ret_status.append("\n**** Exception Occurred: "+str(sys.exc_info()[1])+str(traceback.print_exc()))
    
    print("\n Done \n")
    return ret_status 

#def copyChangesToMaster(src, dest):
    
    #for filename in os.listdir(src):

    #os.path.getmtime(path)

#ret=copyAllToMaster('192.168.1.2','..\\..\\..\\files.zip')
#print(ret)
