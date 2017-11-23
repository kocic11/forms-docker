import env


###########################################################################
# Entry point to the script                                               #
###########################################################################

if (env.HOST_NAME == ''):
    print 'Host name is not properly set.'
    exit(0)

pattern = env.getPattern()

try:
    if env.match(pattern, env.ADMIN_SERVER_NAME):
        try:
            nmConnect(userConfigFile=env.USER_CONFIG_FILE, userKeyFile=env.USER_KEY_FILE, host=env.HOST_NAME, port=env.NM_PORT, domainName=env.DOMAIN_NAME, 
                domainDir=env.DOMAIN_HOME, nmType=env.NM_TYPE)
            nmStart(env.ADMIN_SERVER_NAME) 
        except weblogic.nodemanager.NMException, e:
            pass
        except weblogic.management.scripting.ScriptException, e:
            pass
        except WLSTException, e:
            pass
        except:
            print 'Starting', env.ADMIN_SERVER_NAME, 'failed:', sys.exc_info()[0], sys.exc_info()[1]
    
    connect(userConfigFile=env.USER_CONFIG_FILE, userKeyFile=env.USER_KEY_FILE, url=env.ADMIN_URL)
    env.start(pattern)
except:
    print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]

exit()
