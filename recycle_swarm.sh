#!/usr/bin/env bash

# ./recycle_swarm.sh [-h]
#
# Removes all descriptr services and the node_modules volume
# then rebuilds the images, pushes, and deploys the stack.

# set -e

f_print() { # {{{
    local v_op="$1"
    local v_msg="$2"

    case "$v_op" in
        '-w')
            : "[WARN]"
            ;;
        '-e')
            : "[ERR]"
            ;;
        '-i')
            : "[INFO]"
            ;;
        *)
            v_msg="$v_op"
            : "[INFO]"
            ;;
    esac

    local v_out="$_"
    printf "%s\t%s\n" "$v_out" "$v_msg"
} # }}}

f_usage() { # {{{
    f_print "./recycle_swarm.sh [-h][-n]"
    f_print "-h     Print this help text."
    f_print "-n     Recycle the node_modules volume and assoc. services as well."
    echo "Removes all descriptr services and the node_modules volume" \
        "then rebuilds the images, pushes, and deploys the stack."
    } # }}}

REFRESH_NODE=false

while getopts "hn" options; do
    case "$options" in
        h)
            f_usage
            exit 0
            ;;
        n)
            REFRESH_NODE=true
            ;;
        *)
            f_print -w "Unknown option. Ignoring."
            ;;
    esac
done

if [ "$REFRESH_NODE" = true ]; then
    f_print "Removing docker services"
    docker service rm \
        descriptr_stack_descriptr_api \
        descriptr_stack_descriptr_nginx_load_balancer \
        descriptr_stack_descriptr_web

    f_print "Waiting for clean removal (15)"
    sleep 15
    f_print "Removing node_modules volume"
    docker volume rm descriptr_stack_descriptr_web-node_modules
fi

f_print "Rebuilding images"
docker-compose --verbose -f docker-compose-swarm.dev.yml build
f_print "Pushing"
docker-compose --verbose -f docker-compose-swarm.dev.yml push
f_print "Deploy swarm"
docker stack deploy --compose-file=docker-compose-swarm.dev.yml descriptr_stack
f_print "Swarm deployed, you may need to wait 10-30s for the containers to be fully functional."
