#!/bin/sh
#apk add postfix-lmdb   # alpine
apk add envsubst
apk add postfix-pgsql

# Add env variables to postfix config files
envsubst < /etc/postfix/recipients.cf.template > /etc/postfix/recipients.cf
envsubst < /etc/postfix/virtual.cf.template > /etc/postfix/virtual.cf

# Create postfix lookup tables
postmap /etc/postfix/recipients.cf
postmap /etc/postfix/virtual.cf