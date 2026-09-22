#!/usr/bin/env sh

echo "IP addresses:"
echo "$(ifconfig | grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')"
