#!/bin/sh

echo "Script started: " $(date)

#ORACLE_HOME=/u01/oracle
#JAVA_HOME=/opt/java/jdk1.8.0_131
DOMAIN_ROOT=$ORACLE_HOME/user_projects/domains
DOMAIN_NAME=frm_domain
ADMIN_USER=weblogic
ADMIN_PASSWORD=welcome1
CONNECTION_STRING=192.168.50.101:1521/pdb1
RCUPREFIX=INFRA6
DB_SCHEMA_PASSWORD=welcome1
DOMAIN_HOME=$DOMAIN_ROOT/$DOMAIN_NAME

echo "Removing domain ..."
rm -rf $DOMAIN_ROOT/$DOMAIN_NAME
echo "Domain removed."

echo "Removing repository ..."
$ORACLE_HOME/oracle_common/bin/rcu -silent -dropRepository -connectString $CONNECTION_STRING -dbUser sys -dbRole sysdba -schemaPrefix $RCUPREFIX \
-component IAU \
-component IAU_APPEND \
-component IAU_VIEWER \
-component OPSS \
-component STB \
-component MDS \
-component WLS \
-f < ./passwords
echo "Repository removed."

echo "Creating repository ..."
$ORACLE_HOME/oracle_common/bin/rcu -silent -createRepository -connectString $CONNECTION_STRING -dbUser sys -dbRole sysdba -useSamePasswordForAllSchemaUsers true -schemaPrefix $RCUPREFIX \
-component IAU \
-component IAU_APPEND \
-component IAU_VIEWER \
-component OPSS \
-component STB \
-component MDS \
-component WLS \
-f < ./passwords
echo "Repository created."

echo "Creating domain ..."
$ORACLE_HOME/oracle_common/common/bin/wlst.sh -skipWLSModuleScanning ./createDomain.py -oh $ORACLE_HOME -jh $JAVA_HOME -parent $DOMAIN_ROOT -name $DOMAIN_NAME \
-user $ADMIN_USER -password $ADMIN_PASSWORD -rcuDb $CONNECTION_STRING -rcuPrefix $RCUPREFIX -rcuSchemaPwd $DB_SCHEMA_PASSWORD
echo "Domain created."

echo "Script finished: " $(date)