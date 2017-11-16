#
# Copyright (c) 2016-2017 Oracle and/or its affiliates. All rights reserved.
#
# Licensed under the Universal Permissive License v 1.0 as shown at
# http://oss.oracle.com/licenses/upl.
#

import os
import sys
import time

import com.oracle.cie.domain.script.jython.WLSTException as WLSTException


class FrmProvisioner:

    MACHINES = {
        'machine1': {
            'NMType': 'SSL',
            'ListenAddress': 'localhost',
            'ListenPort': 5656
        },
        'machine2': {
            'NMType': 'SSL',
            'ListenAddress': 'localhost',
            'ListenPort': 5657
        },
        'machine3': {
            'NMType': 'SSL',
            'ListenAddress': 'localhost',
            'ListenPort': 5658
        }

    }

    FORMS_CLUSTERS = {
        'forms_cluster': {}
    }

    RPT_CLUSTERS = {
        'reports_cluster': {}
    }

    SERVERS = {
        'AdminServer': {
            'ListenAddress': '',
            'ListenPort': 7001,
            'Machine': 'machine1'
        }

    }

    FORMS_SERVERS = {
        'WLS_FORMS1': {
            'ListenAddress': '',
            'ListenPort': 9001,
            'Machine': 'machine1',
            'Cluster': 'forms_cluster'
        }
    }

    RPT_SERVERS = {
        'WLS_REPORTS1': {
            'ListenAddress': '',
            'ListenPort': 9002,
            'Machine': 'machine1',
            'Cluster': 'reports_cluster'
        }
    }

    OHS_SERVERS = {
        'OHS_SERVER1': {
            'ListenAddress': '',
            'ListenPort': 8080,
            'SSLListenPort': 443,
            'Machine': 'machine1'
        }
    }

    JRF_12213_TEMPLATES = {
        'baseTemplate': '@@ORACLE_HOME@@/wlserver/common/templates/wls/wls.jar',
        'extensionTemplates': [
            '@@ORACLE_HOME@@/oracle_common/common/templates/wls/oracle.jrf_template.jar',
            '@@ORACLE_HOME@@/oracle_common/common/templates/wls/oracle.jrf.ws.async_template.jar',
            '@@ORACLE_HOME@@/em/common/templates/wls/oracle.em_wls_template.jar'
        ],
        'serverGroupsToTarget': ['JRF-MAN-SVR']
    }

    FORMS_TEMPLATES = {
        'extensionTemplates': [
            '@@ORACLE_HOME@@/forms/common/templates/wls/forms_template.jar'
        ],
        'serverGroupsToTarget': ['FORMS-MAN-SVR']
    }

    RPT_TEMPLATES = {
        'extensionTemplates': [
            '@@ORACLE_HOME@@/ReportsServerComponent/common/templates/wls/oracle.reports_server_template.jar',
            '@@ORACLE_HOME@@/ReportsBridgeComponent/common/templates/wls/oracle.reports_bridge_template.jar',
            '@@ORACLE_HOME@@/reports/common/templates/wls/oracle.reports_app_template.jar'
        ],
        'serverGroupsToTarget': ['REPORTS-APP-SERVERS']
    }

    OHS_TEMPLATES = {
        'extensionTemplates': [
            '@@ORACLE_HOME@@/ohs/common/templates/wls/ohs_managed_template.jar'

        ],
        'serverGroupsToTarget': ['']
    }

    def __init__(self, oracleHome, javaHome, domainParentDir):
        self.oracleHome = self.validateDirectory(oracleHome)
        self.javaHome = self.validateDirectory(javaHome)
        self.domainParentDir = self.validateDirectory(
            domainParentDir, create=True)
        return

    def createDomain(self, name, user, password, db, dbPrefix, dbPassword, domainType):
        domainHome = self.createBaseDomain(name, user, password, domainType)
        self.extendFormsDomain(domainHome, db, dbPrefix, dbPassword)
        self.updateFormMachine(domainName, domainParentDir)
        self.startAdminServer(domainParentDir, domainName, domainUser, domainPassword)
        self.createOhs(domainName, domainParentDir, domainUser, domainPassword)
        self.createReportComponents('reportsToolsInstance1', 'machine1', 'reportsServerInstance1', 'machine1')
        self.deleteDefaultServers(domainUser, domainPassword)
        self.shutdownAdminserverAndNM(domainUser, domainPassword)

    def createBaseDomain(self, name, user, password, domainType):
        baseTemplate = self.replaceTokens(
            self.JRF_12213_TEMPLATES['baseTemplate'])

        readTemplate(baseTemplate)
        setOption('DomainName', name)
        setOption('JavaHome', self.javaHome)
        setOption('ServerStartMode', 'prod')
        set('Name', domainName)
        cd('/Security/' + domainName + '/User/weblogic')
        set('Name', user)
        set('Password', password)

        print 'INFO: Creating Node Managers...'

        # Set NodeManager user name and password
        # ======================================================================
        cd('/')
        create('sc', 'SecurityConfiguration')
        cd('SecurityConfiguration/sc')
        set('NodeManagerUsername', domainUser)
        set('NodeManagerPasswordEncrypted', domainPassword)
        setOption('NodeManagerType', 'PerDomainNodeManager')

        for machine in self.MACHINES:
            cd('/')
            create(machine, 'Machine')
            cd('Machine/' + machine)
            create(machine, 'NodeManager')
            cd('NodeManager/' + machine)
            for param in self.MACHINES[machine]:
                set(param, self.MACHINES[machine][param])

        print 'INFO: Creating Admin server...'

        for server in self.SERVERS:
            cd('/')
            cd('Server/' + server)
            for param in self.SERVERS[server]:
                set(param, self.SERVERS[server][param])
                continue

        print 'INFO: Admin server created.....'

        print 'INFO: Creating Form servers...'

        for cluster in self.FORMS_CLUSTERS:
            cd('/')
            create(cluster, 'Cluster')
            cd('Cluster/' + cluster)
            for param in self.FORMS_CLUSTERS[cluster]:
                set(param, self.FORMS_CLUSTERS[cluster][param])

        for server in self.FORMS_SERVERS:
            cd('/')
            create(server, 'Server')
            cd('Server/' + server)
            for param in self.FORMS_SERVERS[server]:
                set(param, self.FORMS_SERVERS[server][param])

        print 'INFO: Form servers created.....'

        for cluster in self.RPT_CLUSTERS:
            cd('/')
            create(cluster, 'Cluster')
            cd('Cluster/' + cluster)
            for param in self.RPT_CLUSTERS[cluster]:
                set(param, self.RPT_CLUSTERS[cluster][param])

        print 'INFO: Creating Report servers...'

        for server in self.RPT_SERVERS:
            cd('/')
            create(server, 'Server')
            cd('Server/' + server)
            for param in self.RPT_SERVERS[server]:
                set(param, self.RPT_SERVERS[server][param])

        print 'INFO: Report servers created.....'

        setOption('OverwriteDomain', 'true')
        domainHome = self.domainParentDir + '/' + name

        print 'INFO: Writing base domain...'
        writeDomain(domainHome)
        closeTemplate()
        print 'INFO: Base domain created at ' + domainHome
        return domainHome

    def readAndApplyJRFTemplates(self, domainHome):
        print 'INFO: Extending domain at ' + domainHome
        readDomain(domainHome)
        setOption('AppDir', self.domainParentDir + '/applications')

        print 'INFO: Applying JRF templates...'
        for extensionTemplate in self.JRF_12213_TEMPLATES['extensionTemplates']:
            addTemplate(self.replaceTokens(extensionTemplate))
        return

    def applyFormsTemplates(self):
        print 'INFO: Applying Forms templates...'
        for extensionTemplate in self.FORMS_TEMPLATES['extensionTemplates']:
            addTemplate(self.replaceTokens(extensionTemplate))
        return

    def applyReportsTemplates(self):
        print 'INFO: Applying Reports templates...'
        for extensionTemplate in self.RPT_TEMPLATES['extensionTemplates']:
            addTemplate(self.replaceTokens(extensionTemplate))
        return

    def applyOHSTemplates(self):
        print 'INFO: Applying OHS templates...'
        for extensionTemplate in self.OHS_TEMPLATES['extensionTemplates']:
            addTemplate(self.replaceTokens(extensionTemplate))
        return

    def configureJDBCTemplates(self, db, dbPrefix, dbPassword):
        print 'INFO: Configuring the Service Table DataSource...'
        fmwDb = 'jdbc:oracle:thin:@' + db
        cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource')
        cd('JDBCDriverParams/NO_NAME_0')
        set('DriverName', 'oracle.jdbc.OracleDriver')
        set('URL', fmwDb)
        set('PasswordEncrypted', dbPassword)

        stbUser = dbPrefix + '_STB'
        cd('Properties/NO_NAME_0/Property/user')
        set('Value', stbUser)

        print 'INFO: Getting Database Defaults...'
        getDatabaseDefaults()
        return

    def extendFormsDomain(self, domainHome, db, dbPrefix, dbPassword):
        self.readAndApplyJRFTemplates(domainHome)
        self.applyFormsTemplates()
        self.applyReportsTemplates()
        self.applyOHSTemplates()

        print 'INFO: Extension Templates added'

        self.configureJDBCTemplates(db, dbPrefix, dbPassword)

        print 'INFO: Targeting Server Groups...'
        serverGroupsToTarget = list(
            self.JRF_12213_TEMPLATES['serverGroupsToTarget'])
        serverGroupsToTarget.extend(
            self.FORMS_TEMPLATES['serverGroupsToTarget'])
        for server in self.FORMS_SERVERS:
            setServerGroups(server, serverGroupsToTarget)

        serverGroupsToTarget = list(self.RPT_TEMPLATES['serverGroupsToTarget'])
        for server in self.RPT_SERVERS:
            setServerGroups(server, serverGroupsToTarget)

        print 'INFO: Preparing to update domain...'
        updateDomain()
        print 'INFO: Domain updated successfully'
        closeDomain()
        return

    def createOhs(self, domainName, domainParentDir, domainUser, domainPassword):
        print 'INFO: Creating OHS servers...'

        #self.startAdminServer(domainParentDir, domainName, domainUser, domainPassword)

        for server in self.OHS_SERVERS:
            instanceName = server
            machine = self.OHS_SERVERS[server]['Machine']
            listenPort = self.OHS_SERVERS[server]['ListenPort']
            sslPort = self.OHS_SERVERS[server]['SSLListenPort']
            ohs_createInstance(
                instanceName=instanceName, machine=machine, listenPort=listenPort, sslPort=sslPort)

        #self.shutdownAdminserverAndNM()

        print 'INFO: OHS servers created.....'
        return

    def updateFormMachine(self, domainName, domainParentDir):
        adminServer = self.SERVERS['AdminServer']
        adminMachine = adminServer['Machine']

        readDomain(domainParentDir + '/' + domainName)
        cd('SystemComponent/forms1')
        set('Machine', adminMachine)
        updateDomain()
        closeDomain()

    def createBootPropertiesFile(self, domainHome, domainUser, domainPassword):
        securityDir = domainHome + "/servers/" + "AdminServer" + "/security"
        if not os.path.exists(securityDir):
            os.makedirs(securityDir)
            filename = (securityDir + '/' + "boot.properties")
            f = open(filename, 'w')
            line = 'username=' + domainUser + '\n'
            f.write(line)
            line = 'password=' + domainPassword + '\n'
            f.write(line)
            f.close()

    def createReportComponents(self, reportsToolsInstanceName, reportsToolsInstanceMachine, reportsServerInstanceName, reportsServerInstanceMachine):
        print "Creating report components ..."
        #self.startAdminServer(domainParentDir, domainName, domainUser, domainPassword)

        createReportsToolsInstance(
            instanceName=reportsToolsInstanceName, machine=reportsToolsInstanceMachine)
        createReportsServerInstance(
            instanceName=reportsServerInstanceName, machine=reportsServerInstanceMachine)

        #self.shutdownAdminserverAndNM()
        print "Report components created."

    ###########################################################################
    # Helper Methods                                                          #
    ###########################################################################

    def validateDirectory(self, dirName, create=False):
        directory = os.path.realpath(dirName)
        if not os.path.exists(directory):
            if create:
                os.makedirs(directory)
            else:
                message = 'Directory ' + directory + ' does not exist'
                raise WLSTException(message)
        elif not os.path.isdir(directory):
            message = 'Directory ' + directory + ' is not a directory'
            raise WLSTException(message)
        return self.fixupPath(directory)

    def fixupPath(self, path):
        result = path
        if path is not None:
            result = path.replace('\\', '/')
        return result

    def replaceTokens(self, path):
        result = path
        if path is not None:
            result = path.replace('@@ORACLE_HOME@@', oracleHome)
        return result

    def startAdminServer(self, domainParentDir, domainName, domainUser, domainPassword):
        state_admin = nmServerStatus('AdminServer')
        if not (state_admin == 'RUNNING'):
            adminMachine = self.SERVERS['AdminServer']['Machine']
            machineHost = self.MACHINES[adminMachine]['ListenAddress']
            machinePort = self.MACHINES[adminMachine]['ListenPort']
            domainHome = domainParentDir + '/' + domainName
            if (os.system('pgrep -f NodeManager') == 1):
                print "Starting Node Manager ..."
                nmDir = domainParentDir + '/' + domainName + '/nodemanager'
                startNodeManager(verbose='true', NodeManagerHome=nmDir, block='true', username=domainUser, password=domainPassword, host=machineHost,
                                 port=machinePort, domainName=domainName, domainDir=domainHome, nmType='SSL')
                print "Node Manager started."
               
            else:
                print "Node Manager is already running."
            
            domainHome = domainParentDir + '/' + domainName
            
            print "Connecting to Node Manager ..."
            nmConnect(domainUser, domainPassword, machineHost, machinePort, domainName, domainHome,'SSL')
            print "Connected to Node Manager"
                        
            self.createBootPropertiesFile(
                domainHome, domainUser, domainPassword)
            print "Starting Admin server ..."
            nmStart('AdminServer')
            
            adminHost = self.SERVERS['AdminServer']['ListenAddress']
            adminPort = self.SERVERS['AdminServer']['ListenPort']
            if adminHost == '':
                adminHost = 'localhost'
            adminUrl = adminHost + ':' + str(adminPort)
            print "Connecting to Admin Server ..."
            connect(username=domainUser, password=domainPassword, url=adminUrl)

    def deleteDefaultServers(self, domainUser, domainPassword):
        connect(domainUser, domainPassword)
        edit()
        startEdit()
        domain = getMBean('/')

        for name in ['WLS_FORMS', 'WLS_REPORTS']:
            managedServer = domain.lookupServer(name)
            if managedServer != None:
                print 'Deleting server: ', name
                managedServer.setCluster(None)
                managedServer.setMachine(None)
                delete(managedServer.getName(), 'Server')
	
        activate()
        disconnect()

    def shutdownAdminserverAndNM(self, domainUser, domainPassword):
        connect(domainUser, domainPassword)
        shutdown('AdminServer', force='true', block='true')
        stopNodeManager()

#############################
# Entry point to the script #
#############################


def usage():
    print sys.argv[0] + ' -oh <oracle_home> -jh <java_home> -parent <domain_parent_dir> [-name <domain-name>] ' + \
        '[-user <domain-user>] [-password <domain-password>] ' + \
        '-rcuDb <rcu-database> [-rcuPrefix <rcu-prefix>] [-rcuSchemaPwd <rcu-schema-password>] ' + \
        '-domainType <soa|osb|bpm|soaosb> '
    sys.exit(0)


print "createDomain.py called with the following inputs:"
for index, arg in enumerate(sys.argv):
    print "INFO: sys.argv[" + str(index) + "] = " + str(sys.argv[index])

if len(sys.argv) < 6:
    usage()

# oracleHome will be passed by command line parameter -oh.
oracleHome = None
# javaHome will be passed by command line parameter -jh.
javaHome = None
# domainParentDir will be passed by command line parameter -parent.
domainParentDir = None
# domainName is hard-coded to soa_domain. You can change to other name of your choice. Command line parameter -name.
domainName = 'soa_domain'
# domainUser is hard-coded to weblogic. You can change to other name of your choice. Command line paramter -user.
domainUser = 'weblogic'
# domainPassword is hard-coded to welcome1. You can change to other password of your choice. Command line parameter -password.
domainPassword = 'welcome1'
# rcuDb will be passed by command line parameter -rcuDb.
rcuDb = None
# change rcuSchemaPrefix to your soainfra schema prefix. Command line parameter -rcuPrefix.
rcuSchemaPrefix = 'DEV12'
# change rcuSchemaPassword to your soainfra schema password. Command line parameter -rcuSchemaPwd.
rcuSchemaPassword = 'welcome1'

i = 1
while i < len(sys.argv):
    if sys.argv[i] == '-oh':
        oracleHome = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-jh':
        javaHome = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-parent':
        domainParentDir = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-name':
        domainName = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-user':
        domainUser = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-password':
        domainPassword = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-rcuDb':
        rcuDb = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-rcuPrefix':
        rcuSchemaPrefix = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-rcuSchemaPwd':
        rcuSchemaPassword = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == '-domainType':
        domainType = sys.argv[i + 1]
        i += 2
    else:
        print 'INFO: Unexpected argument switch at position ' + str(i) + ': ' + str(sys.argv[i])
        usage()
        sys.exit(1)


provisioner = FrmProvisioner(oracleHome, javaHome, domainParentDir)
provisioner.createDomain(domainName, domainUser, domainPassword,
                         rcuDb, rcuSchemaPrefix, rcuSchemaPassword, domainType)

