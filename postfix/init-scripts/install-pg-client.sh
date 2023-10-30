#!/bin/sh
apk add postfix-pgsql  # alpine
postmap /etc/postfix/recipients.cf
postmap /etc/postfix/virtual.cf