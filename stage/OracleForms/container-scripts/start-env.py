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
			nmStart(env.ADMIN_SERVER_NAME) 
		except:
			print 'Starting', env.ADMIN_SERVER_NAME, 'failed:', sys.exc_info()[0]
	
	connect(userConfigFile=env.USER_CONFIG_FILE, userKeyFile=env.USER_KEY_FILE, url=env.ADMIN_URL)

	cd('/Clusters')
	for cluster in cmo.getClusters():	
		env.start(cluster.getName()):

	cd('/Servers')
	for server in cmo.getServers():
		server_name = server.getName()
		if server_name != env.ADMIN_SERVER_NAME:
			env.start(server_name)

	cd('/SystemComponents')
	for component in cmo.getSystemComponents():
		env.start(component.getName())

except:
	print("Unexpected error: ", sys.exc_info()[0])

exit()
