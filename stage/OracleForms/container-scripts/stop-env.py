import env

###########################################################################
# Entry point to the script                                               #
###########################################################################

if (env.HOST_NAME == ""):
	print("Host name is not properly set.")
	exit(0)
	
try:
	connect(userConfigFile=env.USER_CONFIG_FILE, userKeyFile=env.USER_KEY_FILE, url=env.ADMIN_URL)

	cd('/Clusters')
	for cluster in cmo.getClusters():	
		cluster_name = cluster.getName()
		if env.match(env.PATTERN, cluster_name):
			try:
				shutdown(cluster_name, force='true', block='true')
			except:
				print 'Stopping cluster', cluster_name, 'failed:', sys.exc_info()[0]

	cd('/Servers')
	for server in cmo.getServers():
		server_name = server.getName()
		if server_name != env.ADMIN_SERVER_NAME:
			if env.match(env.PATTERN, server_name):
				try:
					shutdown(server_name, force='true', block='true') 
				except:
					print 'Stopping server', server_name, 'failed:', sys.exc_info()[0]

	cd('/SystemComponents')
	for component in cmo.getSystemComponents():
		component_name = component.getName()
		if env.match(env.PATTERN, component_name):
			try:
				shutdown(component_name, force='true', block='true') 
			except:
				print 'Stopping component', component_name, 'failed:', sys.exc_info()[0]
	# Stop Admin Server
	if env.match(env.PATTERN, env.ADMIN_SERVER_NAME):
		try:
			shutdown(env.ADMIN_SERVER_NAME, force='true', block='true') 
		except:
			print 'Stopping server', env.ADMIN_SERVER_NAME, 'failed:', sys.exc_info()[0]
except:
	print "Unexpected error:", sys.exc_info()[0]
	pass
	
exit()