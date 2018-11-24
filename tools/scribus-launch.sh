#!/bin/bash

USERNAME=`basename $VHOME`
HOMENAME=`dirname $VHOME`

USERID=`ls -lahn $HOME_NAME | grep $USERNAME | awk {'print $3'}`
GROUPID=`ls -lahn $HOME_NAME | grep $USERNAME | awk {'print $4'}`

groupadd -g $GROUPID scribus
useradd --shell /bin/bash --uid $USERID --gid $GROUPID $USERNAME
su $USERNAME -c "/usr/bin/scribus-ng"
