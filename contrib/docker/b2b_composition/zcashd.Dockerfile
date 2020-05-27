FROM          electriccoinco/zcashd:latest
COPY          ./regtest_zcashd.conf /srv/zcashd/.zcash/zcash.conf
RUN           /usr/bin/zcash-fetch-params --testnet
USER          root
COPY          ./regtest_zcashd_entrypoint.sh .
RUN           chmod +x ./regtest_zcashd_entrypoint.sh
RUN           chown zcashd:zcashd ./regtest_zcashd_entrypoint.sh
USER          zcashd
ENTRYPOINT    ["./regtest_zcashd_entrypoint.sh"]