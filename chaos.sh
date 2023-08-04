#!/bin/bash -e

default_services="mongo1,mongo2,mongo3,kafka,zookeeper,connect"
default_signal="SIGKILL"
default_interval=60

# parse arguments
services="$default_services"
signal="$default_signal"

usage() {
    echo "Usage: $0 [-s SIGNAL] [-i INTERVAL] [SERVICE_LIST]"
    echo "  -s SIGNAL      Specify the signal to send to services (default: $default_signal)"
    echo "  -i INTERVAL    Specify the interval between chaos events, in seconds (default: $default_interval)"
    echo "  SERVICE_LIST   Comma-separated list of service names (default: $default_services)"
    exit 1
}

while getopts "si:" opt; do
    case $opt in
        s)
            signal="$OPTARG"
            ;;
        i)
            interval="$OPTARG"
            ;;
        \?)
            usage
            ;;
    esac
done

# Parse argument as service list, if present
shift $((OPTIND - 1))
if [[ $# -gt 0 ]]; then
    services="$1"
fi
IFS=',' read -r -a service_list <<< "$services"

RED='\033[0;31m'
NC='\033[0m' # No Color

while true; do
  echo "Chaos monkey is awake and angry"

  service_index=$((RANDOM % ${#service_list[@]}))
  service="${service_list[service_index]}"

  echo -e "Chaos monkey has chosen: ${RED}$service${NC}"
  docker-compose kill -s $signal $service
  sleep 10
  docker-compose up -d $service

  echo "Chaos monkey is sleeping for $interval seconds..."
  sleep $interval
  echo
done
