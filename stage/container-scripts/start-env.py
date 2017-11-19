import socket 
host_name = socket.gethostbyname(socket.gethostname())
print host_name
url='t3://' + host_name + ':7001'	

if (host_name == ""):
	pritn("Host name is not properly set.")
	exit(0)

try:

	#start Node Manager
	startNodeManager(verbose='true', NodeManagerHome='/u01/app/oracle/admin/domains/bmoris/nodemanager')
	nmConnect(userConfigFile='/home/fradmin/nm.secure', userKeyFile='/home/fradmin/nmkey.secure', host=host_name, port=5556, domainName='bmoris', domainDir='/u01/app/oracle/admin/domains/bmoris', nmType='ssl')

	#Start Admin server
	nmStart('AdminServer')
	
	try:
		connect(userConfigFile='/home/fradmin/admin.secure', userKeyFile='/home/fradmin/adminkey.secure', url=url)
		
		
		#Start Forms and reports
		try:
			start('cluster_forms', type='Cluster', block='true') 	
		except:
			pass
		
		try:
			start('cluster_reports', type='Cluster', block='true')
		except:
			pass
		
		cd('/SystemComponents')
		for component in cmo.getSystemComponents():
			component_type = component.getComponentType()
			if(component_type not in ['FORMS', 'ReportsToolsComponent']):
				try:
					start(component.getName())
				except:
					print "Unexpected error: ", sys.exc_info()[0]
					pass
		
		#disconnect from Admin server
		disconnect()
	except:
		print "Error connecting to AdminSerer: ", sys.exc_info()[0]
		pass
except:
	print "Unexpected error: ", sys.exc_info()[0]
	pass
exit()
