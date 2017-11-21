import env

###########################################################################
# Entry point to the script                                               #
###########################################################################

if (env.HOST_NAME == ""):
    print 'Host name is not properly set.'
    exit(0)

try:
	if env.match(env.PATTERN, env.ADMIN_SERVER_NAME):
		try:
			nmConnect(userConfigFile=env.USER_CONFIG_FILE, userKeyFile=env.USER_KEY_FILE, host=env.HOST_NAME, port=env.NM_PORT, domainName=env.DOMAIN_NAME, 
				domainDir=env.DOMAIN_HOME, nmType=env.NM_TYPE)
			nmStart('AdminServer') 
		except:
			print 'Starting server', env.ADMIN_SERVER_NAME, 'failed:', sys.exc_info()[0]
	
	connect(userConfigFile=env.USER_CONFIG_FILE, userKeyFile=env.USER_KEY_FILE, url=env.ADMIN_URL)

	cd('/Clusters')
	for cluster in cmo.getClusters():	
		cluster_name = cluster.getName()
		if env.match(env.PATTERN, cluster_name):
			try:
				start(cluster_name, block='true')
			except:
				print 'Starting cluster', cluster_name, 'failed:', sys.exc_info()[0]

	cd('/Servers')
	for server in cmo.getServers():
		server_name = server.getName()
		if server_name != env.ADMIN_SERVER_NAME:
			if env.match(env.PATTERN, server_name):
				try:
					start(server_name, block='true') 
				except:
					print 'Starting server', server_name, 'failed:', sys.exc_info()[0]

	cd('/SystemComponents')
	for component in cmo.getSystemComponents():
		component_name = component.getName()
		if env.match(env.PATTERN, component_name):
			try:
				start(component_name, block='true') 
			except:
				print 'Starting component', component_name, 'failed:', sys.exc_info()[0]
except:
	print("Unexpected error: ", sys.exc_info()[0])

exit()
