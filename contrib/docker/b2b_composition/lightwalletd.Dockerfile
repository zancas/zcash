FROM          electriccoinco/lightwalletd:latest
COPY          ./lightwalletd_zcash.conf /srv/lightwalletd/.zcash/zcash.conf
CMD           [ "/usr/local/bin/lightwalletd", \
                "--log-level", "7", \
                "--grpc-bind-addr", "0.0.0.0:9067", \
                "--http-bind-addr", "0.0.0.0:9068", \
                "--no-tls-very-insecure", \
                "--zcash-conf-path", "/srv/lightwalletd/.zcash/zcash.conf", \
                "--data-dir", ".", \
                "--log-file", "/dev/stdout" ]
