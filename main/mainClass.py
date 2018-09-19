'''
Created on Sep 19, 2018

@author: Tony Toms

-----------------DESC-------------------------

Main class
'''

import controller.controllerClass as controller
import config.Config as config
import mastercopy.masterCopy as mastercopy

###########################################################################
retdel=config.deleteConfigNode("192.168.1.2")
retdel2=config.deleteConfigNode("192.168.1.5")
for val in retdel:
    print(val)
for val in retdel2:
    print(val)
#############################################################################    
retcre    =config.createConfigNode('192.168.1.2','192.168.1.5',['test2.py'])
for val in retcre:
    print(val)
#################################################################################
ret4=mastercopy.copyAllToMaster("192.168.1.2","D:\\files.zip")
for val in ret4:
    print(val)    