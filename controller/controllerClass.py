'''
Created on Sep 12, 2018

@author: Tony Toms

-------------Desc:----------------------

This class is executed at controller node.
This class has handlers the node API methods and Backup Node API methods using RMI call

PORT 5050- used for RMI CALLS
PORT 5051- used for file transfer 

'''

import sys
import nodestatus
import os
sys.path.append(".."+os.sep)
import Pyro4
import socket
import utilities.Utilities as utilities
import zipfile
from nodestatus import NodeStatus
import shutil
import io
import threading

def startNodeExecutionHandler(node_ip):
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.startNodeExecution()
    return ret_val
def stopNodeExecutionHandler(node_ip):
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.stopNodeExecution()
    return ret_val
def startBackupNodeExecutionHandler(node_ip):
    backup_node_ip=NodeStatus.getBackupNodeIp(node_ip)
    pyro_proxy=Pyro4.Proxy("PYRO:"+backup_node_ip+".stub@"+backup_node_ip+":5050")
    ret_val=pyro_proxy.startBackupNodeExecution()
    return ret_val

def testNode(node_ip):
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.test()
    return ret_val
def testBackupNode(node_ip):
    backup_node_ip=NodeStatus.getBackupNodeIp(node_ip)
    pyro_proxy=Pyro4.Proxy("PYRO:"+backup_node_ip+".stub@"+backup_node_ip+":5050")
    ret_val=pyro_proxy.testBackupNode()
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
def sendDataToNode(node_ip):
    utilities.createOrReplace(".."+os.sep+"temp")
    if not os.path.isdir(".."+os.sep+"files"+os.sep+node_ip):
        return [False,'ERROR CODE XXXX: Home Directory for node :'+node_ip+" doesn't exist"]
    #zipf = zipfile.ZipFile('../temp/data.zip', 'w', zipfile.ZIP_DEFLATED)
    utilities.zipdir(".."+os.sep+"files"+os.sep+node_ip, ".."+os.sep+"temp"+os.sep+"data")
    
    t = threading.Thread(target=masterFileSender)
    #masterFileSender(node_ip)
    t.start()
    bytesToSend = str(os.path.getsize(".."+os.sep+"temp"+os.sep+"data.zip"))
    pyro_proxy=Pyro4.Proxy("PYRO:"+node_ip+".stub@"+node_ip+":5050")
    ret_val=pyro_proxy.startNodeFileReceiver(nodestatus.NodeStatus.getMasterNodeIP(),bytesToSend)
    return ret_val
    
def sendDataToBackupNode(node_ip):
    utilities.createOrReplace(".."+os.sep+"temp")
    backup_node_ip=NodeStatus.getBackupNodeIp(node_ip)

    if not os.path.isdir(".."+os.sep+"files"+os.sep+backup_node_ip):
        return [False,'ERROR CODE 3001: Home Directory for node :'+backup_node_ip+" doesn't exist"]
    utilities.zipdir(".."+os.sep+"files"+os.sep+backup_node_ip, ".."+os.sep+"temp"+os.sep+"data")
    
    t = threading.Thread(target=masterFileSender)
    #masterFileSender(node_ip)
    t.start()
    bytesToSend = str(os.path.getsize(".."+os.sep+"temp"+os.sep+"data.zip"))
    pyro_proxy=Pyro4.Proxy("PYRO:"+backup_node_ip+".stub@"+backup_node_ip+":5050")
    ret_val=pyro_proxy.startNodeFileReceiver(nodestatus.NodeStatus.getMasterNodeIP(),bytesToSend)
    return ret_val

def masterFileSender():

    data = ".."+os.sep+"temp"+os.sep+"data.zip"
    

    host =nodestatus.NodeStatus.getMasterNodeIP()
    port = 5051

    
    s = socket.socket()
    s.bind((host,port))

    s.listen(5)
    sock, addr = s.accept()
    
    with open(data, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)


#zf = zipfile.ZipFile('../temp/data.zip', "w", zipfile.ZIP_DEFLATED)
#shutil.make_archive('../temp/data', 'zip', "../files/192.168.1.5")

    

#testNode('192.168.1.2')
#sendDataToNode('192.168.1.2')
#loaderNodeHandler('192.168.1.2')
#startNodeExecutionHandler('192.168.1.2')
#stopNodeExecutionHandler('192.168.1.2')


#test()
#sendDataToBackupNode('192.168.1.5')
#loaderBackupNodeHandler('192.168.1.5')
#startBackupNodeExecutionHandler('192.168.1.5')
#stopNodeExecutionHandler('192.168.1.2')