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
		env.stop(cluster.getName())

	cd('/Servers')
	for server in cmo.getServers():
		server_name = server.getName()
		if server_name != env.ADMIN_SERVER_NAME:
			env.stop(server_name)

	cd('/SystemComponents')
	for component in cmo.getSystemComponents():
		env.stop(component.getName())

	# Stop Admin Server
	if env.match(env.PATTERN, env.ADMIN_SERVER_NAME):
		try:
			shutdown(env.ADMIN_SERVER_NAME, force='true', block='true') 
		except:
			print 'Stopping server', env.ADMIN_SERVER_NAME, 'failed:', sys.exc_info()[0]
except:
	print "Unexpected error:", sys.exc_info()[0]
	
exit()