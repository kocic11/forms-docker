import socket, sys, os

DOMAIN_NAME = os.environ('DOMAIN_NAME')

host_name = socket.gethostbyname(socket.gethostname())
print host_name
url='t3://' + host_name + ':7001'	

if (host_name == ""):
	pritn("Host name is not properly set.")
	exit(0)
	
try:
	connect(userConfigFile='/home/fradmin/admin.secure', userKeyFile='/home/fradmin/adminkey.secure', url=url)

	#Shutdown Forms and Reports
	try:
		shutdown('cluster_forms', force='true', block='true')
	except WLSTException:
		pass

	try:
		shutdown('cluster_reports', force='true', block='true')
	except WLSTException:
		pass

	#Shutdown components
	cd('/SystemComponents')
	for component in cmo.getSystemComponents():
		if(component.getComponentType() != 'FORMS'):
			try:
				shutdown(component.getName(), force='true', block='true')
			except:
				print "Unexpected error: ", sys.exc_info()[0]
				pass
		
	#Shutdown Admin server
	try:
		shutdown('AdminServer', force='true', block='true')
	except WLSTException:
		pass

except:
	print "Unexpected error:", sys.exc_info()[0]
	pass

#Shutdown Node Manager
try:
	nmConnect(userConfigFile='/home/fradmin/nm.secure', userKeyFile='/home/fradmin/nmkey.secure', host=host_name, port=5556, domainName='bmoris', domainDir='/u01/app/oracle/admin/domains/bmoris', nmType='ssl')
	stopNodeManager()
except:
	pass
	
exit()