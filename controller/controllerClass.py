'''
Created on Sep 13, 2018

@author: Default
'''
import Pyro4
import socket
import utilities.Utilities as utilities
import os
import zipfile
from nodestatus import NodeStatus

def startNodeExecutionHandler(node_ip):
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.startExecutionNode()
    return ret_val
def stopNodeExecutionHandler(node_ip):
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.stopExecutionNode()
    return ret_val
def startBackupNodeExecutionHandler(node_ip):
    backup_node_ip=NodeStatus.getBackupNodeIp(node_ip)
    pyro_proxy=Pyro4.Proxy("PYRO:"+backup_node_ip+".stub@"+backup_node_ip+":5050")
    ret_val=pyro_proxy.startBackupNodeExecution()
    return ret_val
def stopBackupNodeExecutionHandler(node_ip):
    backup_node_ip=NodeStatus.getBackupNodeIp(node_ip)
    pyro_proxy=Pyro4.Proxy("PYRO:"+backup_node_ip+".stub@"+backup_node_ip+":5050")
    ret_val=pyro_proxy.stopBackupNodeExecution()
    return ret_val
def switchNodeControlHandler(node_ip,mode):
    print("hei")
def loaderNodeHandler(node_ip):
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.loaderNode()
    return ret_val    
def loaderBackupNodeHandler(node_ip):
    backup_node_ip=NodeStatus.getBackupNodeIp(node_ip)
    pyro_proxy=Pyro4.Proxy("PYRO:"+backup_node_ip+".stub@"+backup_node_ip+":5050")
    ret_val=pyro_proxy.loaderBackupNode()
    return ret_val
def sendFileNode(node_ip):
    utilities.createOrReplace("../temp")
    if not os.path.isdir("../files/"+node_ip):
        return [False,'ERROR CODE XXXX: Home Directory for node :'+node_ip+" doesn't exist"]
    zipf = zipfile.ZipFile('../temp/data.zip', 'w', zipfile.ZIP_DEFLATED)
    utilities.zipdir("../files/"+node_ip, zipf)
    zipf.close()
    
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.startNodeFileReceiver(node_ip)
    masterFileSender(node_ip)
    
def sendFileBackupNode(node_ip):
    backup_node_ip=NodeStatus.getBackupNodeIp(node_ip)
    utilities.createOrReplace("../temp")
    if not os.path.isdir("../files/"+node_ip):
        return [False,'ERROR CODE XXXX: Home Directory for node :'+node_ip+" doesn't exist"]
    zipf = zipfile.ZipFile('../temp/data.zip', 'w', zipfile.ZIP_DEFLATED)
    utilities.zipdir("../files/"+node_ip, zipf)
    zipf.close()
    
    pyro_proxy=Pyro4.Proxy("PYRO:"+backup_node_ip+".stub@"+backup_node_ip+":5050")
    ret_val=pyro_proxy.startBackupNodeFileReceiver(backup_node_ip)
    masterFileSender(backup_node_ip)

def masterFileSender(node_ip):
    HOST = node_ip
    PORT = 5051
    ADDR = (HOST,PORT)
    BUFSIZE = 4096
    
    data = "../temp/data.zip"
    bytes = open(data).read()
    #print (len(bytes))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(bytes.encode())
    client.close()