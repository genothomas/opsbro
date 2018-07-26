#!/usr/bin/env bash

# Load common shell functions
MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $MYDIR/common_shell_functions.sh



/etc/init.d/postfix start

# We do force a compliance error
chmod 777 /etc/passwd

/etc/init.d/opsbro start

sleep 5

print_header "Starting to test MAIL handlers"

NB_EMAILS_DEFERED=$(find /var/spool/postfix/defer* -type f | wc -l)
NB_EMAILS_ACTIVE=$(find /var/spool/postfix/active -type f | wc -l)


if [ $NB_EMAILS_DEFERED -eq 0 ] && [ $NB_EMAILS_ACTIVE -eq 0 ]; then
    echo "There is no mail generated by handlers, error active=$NB_EMAILS_ACTIVE  defered*=$NB_EMAILS_DEFERED "
    cat /var/log/opsbro/module.mail.log
    exit 2
fi

print_header "Emails: Defered:$NB_EMAILS_DEFERED   Active:$NB_EMAILS_ACTIVE "

echo "DEFERED"
cat /var/spool/postfix/defer*/*/*
echo "ACTIVE"
cat /var/spool/postfix/active/*

# Should have en email from compliance too
grep --text -r compliance /var/spool/postfix | grep --text 'passwd is root/644'
if [ $? != 0 ];then
   echo "ERROR: we should have en email about the passwd is root/644 compliance rule, but none is founded"
   opsbro compliance history
   cat /var/log/opsbro/module.mail.log
fi

print_header "Email handler OK"
