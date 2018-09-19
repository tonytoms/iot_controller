'''
Created on Sep 7, 2018

@author: Tony Toms

--------------DESC-------------------------------
This class contains methods to alter configuration settings

----------------main variables--------------
# ret_status-  this list has all the informations regarding the running of each method. this variable is returned to the controller at the end
            ret_status[0] - True if task completed and false if an issue occurred
--------------------------------------

'''


import xml.etree.ElementTree as ElementTree
from nodestatus import NodeStatus
import sys
import os as os
import shutil
import utilities.Utilities as utilities
import nodestatus
import traceback


#This function Deletes the Node configuration Settings
def deleteConfigNode( node_ip):
    
    ret_status=[True,"Step 1(of 4) - Getting config.xml","Step 2(of 4) - Removing node from config.xml","Step(3 of 4) - Deleting Node Files"
                ,"Step 4(of 4) - Removing Backup Node Files "]
    print("\n Running deleteConfigNode() \n")  
    
    try: 
        values=NodeStatus.getNodeList()   
        tree = ElementTree.parse(".."+os.sep+"config.xml")  
        ret_status[1]=ret_status[1]+" :Done"
        
        root = tree.getroot()
        check=False
        backup_node_ip=nodestatus.NodeStatus.getBackupNodeIp(node_ip)
    
        ############# Removing the Child ##############################
        for child in root:
            if len(child)>0:
                
                if child[0].text != node_ip:
                    continue
                else:
                    root.remove(child)
                    tree.write(".."+os.sep+"config.xml")
                    
                    check=True
                    
        if not check:
            ret_status[2]=ret_status[2]+" : no node with the IP Address"
        else:
            ret_status[2]=ret_status[2]+" : Done"
            
        ############# Removing the Folders  ##############################
        if(os.path.exists(".."+os.sep+"files"+os.sep +node_ip)):
            shutil.rmtree(".."+os.sep+"files"+os.sep +node_ip)
            ret_status[3]=ret_status[3]+" :Done"
        else:
            ret_status[3]=ret_status[3]+" :No Folder for the IP Address"
            
            
        if(os.path.exists(".."+os.sep+"files"+os.sep +backup_node_ip)):
            shutil.rmtree(".."+os.sep+"files"+os.sep +backup_node_ip) 
            ret_status[4]=ret_status[4]+" :Done"
        else:
            ret_status[4]=ret_status[4]+" :No backup Node Folder for the IP Address"  
            
    except:
        ret_status[0]=False
        ret_status.append("\n**** Exception Occurred: "+str(sys.exc_info()[1])+str(traceback.print_exc()))
        
    print("\n Done \n")
    return ret_status  


#This Function Creates a Configuration Node
def createConfigNode( node_ip, backup_node_ip,executableList=[]):
    
    ret_status=[True,"Step 1(of 5) - Getting config.xml","Step 2(of 5) - Checking Config File","Step(3 of 5) - Creating Node Folders"
                ,"Step 4(of 5) - Writing to Node Config Files","Step 5(of 5) - Writing to main Config File"]
    print("\n Running createConfigNode() \n")      
    
    try:
        values=NodeStatus.getNodeList()   
        tree = ElementTree.parse(".."+os.sep+"config.xml") 
        ret_status[1]=ret_status[1]+" Done"
         
        root = tree.getroot()
        if node_ip in values:
            ret_status[0]=False
            ret_status[2] =ret_status[2] +'ERROR CODE 1003: Node with Ip Address :'+node_ip+" already present in config.xml"
            return ret_status
        else:
            ret_status[2]=ret_status[2]+" : Done"
            node_element = ElementTree.Element('node')
            
            node_ip_element = ElementTree.Element('nip')
            node_ip_element.text=node_ip
            node_bip_element = ElementTree.Element('nbip')
            node_bip_element.text=backup_node_ip
            node_executable_element = ElementTree.Element('executables')
            
            executable_files=[]
            for files in executableList[:]:
                node_file_element = ElementTree.Element('file')
                node_file_element.text=files           
                node_executable_element.append(node_file_element)
             
            node_element.append(node_ip_element)
            node_element.append(node_bip_element)
            node_element.append(node_executable_element)
            
            root.append(node_element)
            tree = ElementTree.ElementTree(root)
            
            
            ########## Creating Folders for the nodes  ##############################
            utilities.checkExistOrCreate(".."+os.sep+"files")
            path = ".."+os.sep+"files"+os.sep+node_ip
            pathbkup = ".."+os.sep+"files"+os.sep+backup_node_ip
            utilities.createOrReplace(path)
            utilities.createOrReplace(pathbkup)
            ret_status[3] =ret_status[3] +" : Done"
            
            
            ########## Writing to all the config files  ##############################
            child_root=ElementTree.Element("client")
            child_root.append(node_element)
            
            tree_child = ElementTree.ElementTree(child_root) 
            tree_child.write(path+os.sep+"configClient.xml")
            tree_child.write(pathbkup+os.sep+"configClient.xml")
            ret_status[4] =ret_status[4] +" : Done"
            
            tree.write(".."+os.sep+"config.xml")
            ret_status[5] =ret_status[5] +" : Done"
                   
        
    except:
        ret_status[0]=False
        ret_status.append("\n**** Exception Occurred: "+str(sys.exc_info()[1])+str(traceback.print_exc()))
    
    print("\n Done \n")
    return ret_status 
    
#This Function Updates the node Configuration           
def updateConfigNode( node_ip, backup_node_ip,executableList=[]):

    ret_status=[True,"Step 1(of 3) - Getting config.xml","Step 2(of 4) - Checking Config File","Step 3(of 4) - Calling deleteConfigNode()","Step(4 of 4) - Calling createConfigNode()"]
    print("\n Running updateConfigNode() \n")      
    
    try:    
        values=NodeStatus.getNodeList()   
        tree = ElementTree.parse(".."+os.sep+"config.xml")
        ret_status[1]=ret_status[1]+" :Done"
          
        root = tree.getroot()
        if node_ip not in values:
            ret_status[0]=False
            ret_status[2]=ret_status[2]+ 'ERROR CODE 1004: Node with Ip Address :'+node_ip+" not found in config.xml"
            return
        
        else:
            ret_status[2]=ret_status[2]+" : Done"
            
            RetValDel=deleteConfigNode(node_ip)  #####CALLING DELETE NODE
            if not RetValDel[0]:
                ret_status[0]=False
                ret_status.append("Appending Status of deleteConfigNode()")
                ret_status=ret_status+RetValDel
                return ret_status
                
            else:
                ret_status[3]=ret_status[3]+" : Done"
                retValCre=createConfigNode(node_ip, backup_node_ip,executableList)    #######CALLING CREATE NODE
                if not retValCre[0]:
                    ret_status[0]=False
                    ret_status.append("Appending Status of createConfigNode()")
                    ret_status=ret_status+RetValDel
                    return ret_status
                
                ret_status[4]=ret_status[4]+" : Done"
    except:
        ret_status[0]=False
        ret_status.append("\n**** Exception Occurred: "+str(sys.exc_info()[1])+str(traceback.print_exc()))
    
    print("\n Done \n")
    return ret_status #deleteConfigNode('192.168.1.5')
#deleteConfigNode('192.168.1.2')
#createConfigNode('192.168.1.2','192.168.1.5',['test2.py'])
#ret=updateConfigNode('192.168.1.2','192.168.1.5',['test1.py','test2.py'])
#print(ret)
