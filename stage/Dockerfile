# HOW TO BUILD THIS IMAGE
# -----------------------
# The Oracle Forms and Reports image extends the FMW Infrastructure 12.2.1.3 image.
# Run: 
#      $ docker build --force-rm=true --no-cache=true -t akocic/forms:12.2.1.3 -f Dockerfile .
#      $ docker run -d -p 7001:7001 -p 9002:9002 -p 9001:9001 -p 8080:8080 -p 443:443 -v /vagrant/stage:/u01/oracle/user_projects --name formsadmin --env-file ./infraDomain.env.list akocic/forms:12.2.1.3

#
# IMPORTANT
# ---------
# The resulting image of this Dockerfile contains Forms and Reports Domain.
#
# From 
# -------------------------
FROM oracle/fmw-infrastructure:12.2.1.3

# Maintainer
# ----------
MAINTAINER Kocic


# Common environment variables required for this build 
# ----------------------------------------------------
ENV ORACLE_HOME=/u01/oracle \
    SCRIPT_FILE=${ORACLE_HOME}/container-scripts/* \
    USER_MEM_ARGS="-Djava.security.egd=file:/dev/./urandom" \
    DOMAIN_NAME="${DOMAIN_NAME:-InfraDomain}" \
    DOMAIN_HOME=${ORACLE_HOME}/user_projects/domains/${DOMAIN_NAME:-InfraDomain} \
    VOLUME_DIR=${ORACLE_HOME}/user_projects \
    PATH=$PATH:/usr/java/default/bin:${ORACLE_HOME}/oracle_common/common/bin:${ORACLE_HOME}/wlserver/common/bin:${ORACLE_HOME}/container-scripts


#USER root    
# Setup subdirectory for FMW install package and container-scripts
# -----------------------------------------------------------------  
USER root
# Copy packages and scripts
# -------------
COPY container-scripts/* ${ORACLE_HOME}/container-scripts/

# Environment variables required for this build (do NOT change)
# -------------------------------------------------------------
ENV FMW_PKG1=fmw_12.2.1.3.0_fr_linux64_Disk1_1of2.zip \
    FMW_PKG2=fmw_12.2.1.3.0_fr_linux64_Disk1_2of2.zip \
    FMW_BIN=fmw_12.2.1.3.0_fr_linux64.bin

# Copy binaries and install required packages
# -------------
COPY $FMW_PKG1 $FMW_PKG2 install.file oraInst.loc /u01/
RUN sed -i 's|securerandom.source=file:/dev/random|securerandom.source=file:/dev/urandom|' $JAVA_HOME/jre/lib/security/java.security && \
    chown oracle:oracle -R /u01 && \
    chmod +xr $SCRIPT_FILE && \
    yum -y install\
        compat-libcap1\
        binutils\
        compat-libstdc++\
        compat-libstdc++\
        gcc\
        gcc-c++\
        glibc\
        glibc-devel\
        libaio\
        libaio-devel\
        libgcc\
        libstdc++\
        libstdc++-devel\
        libXrender\
        libXtst\
        ksh\
        make\
        sysstat\
        numactl\
        numactl-devel\
        motif\
        motif-devel\ 
        dos2unix\ 
        unzip &&\
    rm -rf /var/cache/yum && \
    mkdir -p $VOLUME_DIR && \
    chown -R oracle:oracle $VOLUME_DIR

VOLUME  $VOLUME_DIR

# Install 
# ------------------------------------------------------------
USER oracle
RUN cd /u01/ && \
    unzip -o $FMW_PKG1 && \
    unzip -o $FMW_PKG2 && \
    ./$FMW_BIN -silent -responseFile /u01/install.file -invPtrLoc /u01/oraInst.loc -jreLoc $JAVA_HOME -force \
    ORACLE_HOME=$ORACLE_HOME INSTALL_TYPE="Forms and Reports Deployment" && \
    rm /u01/$FMW_PKG1 /u01/oraInst.loc /u01/install.file

WORKDIR ${ORACLE_HOME}

# Define default command to start script.
CMD ["container-scripts/createInfraDomainAndStartAdmin.sh"]