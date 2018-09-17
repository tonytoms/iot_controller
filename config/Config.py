import xml.etree.ElementTree as ElementTree
from nodestatus import NodeStatus
import lxml.etree as etree
import os as os
import shutil
import utilities.Utilities as utilities
import nodestatus

'''
Created on Sep 7, 2018

@author: Default
'''

def deleteConfigNode( node_ip):
    values=NodeStatus.getNodeList()   
    tree = ElementTree.parse("..\config.xml")  
    root = tree.getroot()
    check=False
    backup_node_ip=nodestatus.NodeStatus.getBackupNodeIp(node_ip)

    for child in root:
        if len(child)>0:
            
            if child[0].text != node_ip:
                continue
            else:
                root.remove(child)
                tree.write("..\config.xml")
                check= True
                
    
    
    if(os.path.exists("../files/" +node_ip)):
        shutil.rmtree("../files/" +node_ip)
    if(os.path.exists("../files/" +backup_node_ip)):
        shutil.rmtree("../files/" +backup_node_ip)   
    
    return [True,'']


def createConfigNode( node_ip, backup_node_ip,executableList=[]):
    values=NodeStatus.getNodeList()   
    tree = ElementTree.parse("..\config.xml")  
    root = tree.getroot()
    if node_ip in values:
        return [False,'ERROR CODE 1003: Node with Ip Address :'+node_ip+" already present in config.xml"]
    else:
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
        
        
        utilities.checkExistOrCreate("../files")
        path = "../files/"+node_ip
        pathbkup = "../files/"+backup_node_ip
        utilities.createOrReplace(path)
        utilities.createOrReplace(pathbkup)
        
        child_root=ElementTree.Element("client")
        child_root.append(node_element)
        tree_child = ElementTree.ElementTree(child_root) 
        tree_child.write(path+"/configClient.xml")
        tree_child.write(pathbkup+"/configClient.xml")

        tree.write("..\config.xml")
        
               
        
        return True
       
def updateConfigNode( node_ip, backup_node_ip,executableList=[]):
    values=NodeStatus.getNodeList()   
    tree = ElementTree.parse("..\config.xml")  
    root = tree.getroot()
    if node_ip not in values:
        return [False,'ERROR CODE 1004: Node with Ip Address :'+node_ip+" not found in config.xml"]
    else:
        deleteConfigNode(node_ip)
        createConfigNode(node_ip, backup_node_ip,executableList)
        return True
deleteConfigNode('192.168.1.5')
createConfigNode('192.168.1.5','192.168.1.2',['test2.py'])
#updateConfigNode('192.168.1.2','192.168.1.5',['test1.py','test2.py'])
