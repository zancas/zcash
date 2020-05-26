FROM          electriccoinco/zcashd:latest
COPY          ./regtest_node_zcash.conf /srv/zcashd/.zcash/zcash.conf
ENTRYPOINT    ["/usr/bin/zcashd", "-printtoconsole"]
