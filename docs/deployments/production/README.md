============================================
# ORIGINAL SERVER CONFIGURATION - ALREADY DONE :)
## NO NEED TO DO AGAIN
============================================

1. SSH into the socs machine
```
$ ssh sysadmin@cis4250-03.socs.uoguelph.ca
```
password: <password_for_server>

2. Open up required ports:

```
$ sudo apt install ufw
$ sudo ufw allow 22
$ sudo ufw allow 2376/tcp
$ sudo ufw allow 2377/tcp
$ sudo ufw allow 7946/tcp
$ sudo ufw allow 7946/udp
$ sudo ufw allow 4789/udp
$ sudo ufw allow 80/tcp
$ sudo ufw allow 443/tcp

$ sudo ufw enable
```

3. Make the sysadmin user a sudoer

```
$ sudo nano /etc/sudoers
```
Add the following line below the "#includedir /etc/sudoers.d" line:

```
sysadmin ALL=(ALL) NOPASSWD: ALL
```

=============================
# DEPLOYING - FIRST TIME DEPLOY
=============================

1. If you don't already have a keypair you're ok with using, create a new ssh key pair:

On your laptop run:

```
$ cd ~/.ssh
$ ssh-keygen -t rsa
```

Name it descriptr-manager-1-id_rsa and don't give it a passphrase.

2. Copy the public key to the server

```
$ ssh-copy-id -i descriptr-manager-1-id_rsa.pub sysadmin@cis4250-03.socs.uoguelph.ca
```
Type in the password for the sysadmin user(The one greg gave us)

3. Make the machine a docker machine:

```
$ docker-machine create \
	--driver generic \
	--generic-ip-address=cis4250-03.socs.uoguelph.ca \
	--generic-ssh-user sysadmin \
	--generic-ssh-key ~/.ssh/descriptr-manager-1-id_rsa \
	descriptr-manager-1
```

4. Initialize the swarm master

```
$ docker-machine ssh descriptr-manager-1
$ sudo docker swarm init
$ exit
```

5. continue below...

==================================
# DEPLOYING - SUBSEQUENT DEPLOYMENTS
==================================

## REQUIRED CHECKS:
----------------
Check that you have the dummy development certificate: docker/nginx_load_balancer/nginx/ssl/dev.full.pem & docker/nginx_load_balancer/nginx/ssl/dev.key.pem.
ONLY IF you don't: Create a self signed certificate for development:

```
$ openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
  -keyout docker/nginx_load_balancer/nginx/ssl/dev.key.pem -out docker/nginx_load_balancer/nginx/ssl/dev.full.pem -subj "/CN=parklotti.com" \
  -addext "subjectAltName=DNS:parklotti.com,DNS:*.parklotti.com,IP:10.0.0.1"
```

This certificate will be deployed to production and then written over by acme.sh

## DEPLOYMENT:
-----------

```
$ cd <project_dir>
$ sudo docker-compose -f docker-compose-swarm.prod.yml build
$ sudo docker login registry.hub.docker.com
```

(This is using max's docker hub so you don't have the login details - Maybe ask him to change the password)

```
$ sudo docker push registry.hub.docker.com/steepvisions/uog-course-descriptions-descriptr_web
$ sudo docker push registry.hub.docker.com/steepvisions/uog-course-descriptions-descriptr_api
$ sudo docker push registry.hub.docker.com/steepvisions/uog-course-descriptions-descriptr_nginx_load_balancer
$ sudo docker push registry.hub.docker.com/steepvisions/uog-course-descriptions-descriptr_acmesh

$ docker-machine env descriptr-manager-1 && eval $(docker-machine env descriptr-manager-1) && clear && docker-machine ls

$ env $(cat .env | grep ^[A-Z] | xargs) docker stack deploy --with-registry-auth --compose-file=docker-compose-swarm.prod.yml descriptr_stack
```

Wait a bit and check if services are running. Should never be 0/<some_num>
```
$ docker-machine ssh descriptr-manager-1
$ sudo docker stack services descriptr_stack
```