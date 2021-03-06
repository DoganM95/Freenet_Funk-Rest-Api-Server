#!/bin/sh

# Echo if a environment varible is not passed in run command
if [ -z ${FUNK_USERNAME} ]; then
    echo 'Please define a username using docker run -e "FUNK_USERNAME=<your_ewelink_username>" -e ...'
elif [ -z ${FUNK_PASSWORD} ]; then
    echo 'Please define a password using docker run -e "FUNK_PASSWORD=<your_ewelink_password>" -e ...'
else
    cd /usr/src/app
    sed -i "s/funk_username = .*/funk_username = '$FUNK_USERNAME'/g" ./configuration/credentials.py
    sed -i "s/funk_password = .*/funk_password = '$FUNK_PASSWORD'/g" ./configuration/credentials.py
fi

# Run Node js server code
python ./server.py
