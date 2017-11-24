import socket
import os
import re
import sys
import wl
from sets import Set

# Domain
DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'forms')
DOMAIN_HOME = os.getenv('DOMAIN_HOME', '/u01/oracle/user_projects/domains/forms')

# Security
USER_CONFIG_FILE = os.getenv('USER_CONFIG_FILE', '/u01/oracle/userConfigFile')
USER_KEY_FILE = os.getenv('USER_KEY_FILE', '/u01/oracle/userKeyFile')

# Node Manager
NM_PORT =  os.getenv('NM_PORT', 5656)
NM_TYPE = os.getenv('NM_TYPE', 'SSL')

# Host name
HOST_NAME = 'localhost'  # socket.gethostbyname(socket.gethostname())

# Admin server
ADMIN_PORT = os.getenv('ADMIN_PORT', '7001')
ADMIN_URL = 't3://' + HOST_NAME + ':' + ADMIN_PORT
ADMIN_SERVER_NAME = os.getenv('ADMIN_SERVER_NAME', 'AdminServer')

###########################################################################
# Helper Methods                                                          #
###########################################################################

def getPattern():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return ''

def match(pattern, name):
    matchObject = re.compile(pattern).match(name)
    if matchObject != None and matchObject.group(0) != '':
        return True
    return False


def start(pattern):
    for nameState in getNameState(pattern):
        nameStateList = nameState.split(':')
        if nameStateList[1] != 'RUNNING':
            try:
                wl.start(nameStateList[0], block='true')
            except:
                print 'Starting', nameStateList[0], 'failed:', sys.exc_info()[0], sys.exc_info()[1] 

def stop(pattern):
    for nameState in getNameState(pattern):
        nameStateList = nameState.split(':')
        if nameStateList[1] == 'RUNNING':
            try:
                wl.shutdown(nameStateList[0], force='true', block='true')
            except:
                print 'Stopping', nameStateList[0], 'failed:', sys.exc_info()[0], sys.exc_info()[1]

def getNameState(pattern):
    names = []
    wl.cd('/Clusters')
    for cluster in wl.cmo.getClusters():
        if match(pattern, cluster.getName()):
            for server in cluster.getServers():
                wl.domainRuntime()   
                wl.cd('/ServerLifeCycleRuntimes')
                names.append(server.getName() + ':' + wl.cmo.lookupServerLifeCycleRuntime(server.getName()).getState())
    
    wl.domainRuntime()   

    wl.cd('/ServerLifeCycleRuntimes')
    names.extend([server.getName() + ':' + server.getState() for server in wl.cmo.getServerLifeCycleRuntimes() if match(pattern, server.getName()) 
        and server.getName() != ADMIN_SERVER_NAME])      
    
    wl.cd('/SystemComponentLifeCycleRuntimes')
    names.extend([component.getName() + ':' + component.getState() for component in wl.cmo.getSystemComponentLifeCycleRuntimes() if match(pattern, component.getName())])
    
    names = list(Set(names))
    print 'Names and states:', names
    return names