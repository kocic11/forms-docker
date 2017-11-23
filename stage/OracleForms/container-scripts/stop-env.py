import env

###########################################################################
# Entry point to the script                                               #
###########################################################################

if (env.HOST_NAME == ""):
    print('Host name is not properly set.')
    exit(0)

pattern = env.getPattern()

try:
    connect(userConfigFile=env.USER_CONFIG_FILE, userKeyFile=env.USER_KEY_FILE, url=env.ADMIN_URL)
    env.stop(pattern)
    
    # Stop Admin Server
    if env.match(pattern, env.ADMIN_SERVER_NAME):
        try:
            shutdown(env.ADMIN_SERVER_NAME, force='true', block='true') 
        except:
            print 'Stopping', env.ADMIN_SERVER_NAME, 'failed:', sys.exc_info()[0]
except:
    print 'Unexpected error:', sys.exc_info()[0]
    
exit()