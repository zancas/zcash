FROM          electriccoinco/zcashd:latest
COPY          ./regtest_node_zcash.conf /srv/zcashd/.zcash/zcash.conf
RUN           /usr/bin/zcash-fetch-params --testnet
USER          root
RUN           apt-get update && apt-get install -y vim procps
COPY          ./regtest_zcashd_entrypoint.sh .
RUN           chmod +x ./regtest_zcashd_entrypoint.sh
RUN           chown zcashd:zcashd ./regtest_zcashd_entrypoint.sh
USER          zcashd
ENTRYPOINT    ["./regtest_zcashd_entrypoint.sh"]
