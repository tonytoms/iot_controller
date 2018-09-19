'''
Created on Sep 7, 2018

@author: Tony Toms
This class contains supporting methods for node status

'''


import xml.etree.ElementTree as ElementTree  
import os

#This function returns a list of IP addresses of primary nodes
def getNodeList():
    tree = ElementTree.parse(".."+os.sep+"config.xml")  
    root = tree.getroot()
    values = [e.text for e in root.findall("node/nip")]
    return values

#This function returns a list of IP addresses of backup nodes
def getBackupNodeList():
    tree = ElementTree.parse(".."+os.sep+"config.xml")  
    root = tree.getroot()
    values = [e.text for e in root.findall("node/bnip")]
    return values
def getBackupNodeIp(node_ip):
    tree = ElementTree.parse(".."+os.sep+"config.xml")  
    root = tree.getroot()
    for child in root:
        if len(child)>0:
                
                if child[0].text == node_ip:
                    return(child[1].text) 
    return("")            
def getMasterNodeIP():
    tree = ElementTree.parse(".."+os.sep+"config.xml")  
    root = tree.getroot()
    return root[0].text
                  