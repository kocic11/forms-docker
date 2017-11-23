import socket
import os
import re
import sys
import wl

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
ADMIN_PORT = os.getenv('ADMIN_PORT', '7002')
ADMIN_URL = 't3s://' + HOST_NAME + ':' + ADMIN_PORT
ADMIN_SERVER_NAME = os.getenv('ADMIN_SERVER_NAME', 'AdminServer')

###########################################################################
# Helper Methods                                                          #
###########################################################################

def getPattern():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return ''

def match(pattern, name):
    return re.compile(pattern).match(name)


def start(pattern):
    for name in getNames(pattern):
        try:
            wl.start(name, block='true')
        except wl.NMException, e:
            pass
        except wl.ScriptException, e:
            pass
        except wl.WLSTException, e:
            pass
        except:
            print 'Starting', name, 'failed:', sys.exc_info()[0], sys.exc_info()[1] 

def stop(pattern):
    for name in getNames(pattern):
        try:
            wl.shutdown(name, force='true', block='true')
        except wl.WLSTException, e:
            pass
        except:
            print 'Stopping', name, 'failed:', sys.exc_info()[0], sys.exc_info()[1]

def getNames(pattern):
    wl.cd('/Clusters')
    names = [cluster.getName() for cluster in wl.cmo.getClusters() if match(pattern, cluster.getName())]

    wl.cd('/Servers')
    names.extend([server.getName() for server in wl.cmo.getServers() if match(pattern, server.getName()) and server.getName() != ADMIN_SERVER_NAME])

    wl.cd('/SystemComponents')
    names.extend([component.getName() for component in wl.cmo.getSystemComponents() if match(pattern, component.getName())])
    
    return names
