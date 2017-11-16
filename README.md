# forms-docker
HOW TO BUILD THIS IMAGE
-----------------------
The Oracle Forms and Reports image extends the FMW Infrastructure 12.2.1.3 image.

Build:

docker build --force-rm=true --no-cache=true -t akocic/forms:12.2.1.3 -f Dockerfile .

Run:

docker run -d -p 7001:7001 -p 9002:9002 -p 9001:9001 -p 8080:8080 -p 443:443 -v /vagrant/stage:/u01/oracle/user_projects --name formsadmin --env-file ./infraDomain.env.list akocic/forms:12.2.1.3

IMPORTANT
---------
The resulting image of this Dockerfile contains Forms and Reports Domain.
