import socket
import os
import re

DOMAIN_NAME = os.getenv('DOMAIN_NAME','forms')
DOMAIN_HOME = os.getenv('DOMAIN_HOME','/u01/oracle/user_projects/domains/forms')
USER_CONFIG_FILE = os.getenv('USER_CONFIG_FILE', '/u01/oracle/userConfigFile')
USER_KEY_FILE = os.getenv('USER_KEY_FILE','/u01/oracle/userKeyFile')
NM_PORT = 5656
NM_TYPE = os.getenv('NM_TYPE','SSL')
ADMIN_PORT = os.getenv('ADMIN_PORT', '7001')
HOST_NAME = 'localhost'  # socket.gethostbyname(socket.gethostname())
ADMIN_URL = 't3://' + HOST_NAME + ':' + ADMIN_PORT
ADMIN_SERVER_NAME = os.getenv('ADMIN_SERVER_NAME', 'AdminServer')

PATTERN = os.getenv('PATTERN')


###########################################################################
# Helper Methods                                                          #
###########################################################################

def match(pattern, name):
    if pattern != None:
    	pattern = re.compile(pattern)
    	return pattern.match(name)
	return True