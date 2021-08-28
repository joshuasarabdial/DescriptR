#!/bin/sh

if [ ! -d "/acme.sh/cis4250-03.socs.uoguelph.ca" ]; then
	echo 'First startup'
    echo 'Asking for certificates'
	acme.sh --issue -d "cis4250-03.socs.uoguelph.ca" -w /home/ubuntu/acme-challenge

	echo 'Deploying certificate:'
	acme.sh --deploy -d "cis4250-03.socs.uoguelph.ca" --deploy-hook docker
fi

echo 'Listing certs'
acme.sh --list
# Make the container keep running
/entry.sh daemon