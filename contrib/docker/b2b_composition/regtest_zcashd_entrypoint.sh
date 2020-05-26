#! /bin/bash

set -ex
/usr/bin/zcashd -printtoconsole &
sleep 6
/usr/bin/zcash-cli --verbose generate 1
wait
