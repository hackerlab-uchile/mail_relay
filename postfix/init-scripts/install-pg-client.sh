#!/bin/sh
apk add postfix-pgsql
postmap /etc/postfix/recipients.cf
postmap /etc/postfix/virtual.cf