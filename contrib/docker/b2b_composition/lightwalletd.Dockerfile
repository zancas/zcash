FROM          golang:1.14.3
RUN           mkdir -p /go/src/github.com/zcash/
WORKDIR       /go/src/github.com/zcash/
RUN           git clone https://github.com/zcash/lightwalletd.git
WORKDIR       /go/src/github.com/zcash/lightwalletd
RUN           make build \
                && /usr/bin/install -c ./lightwalletd /usr/local/bin/

ARG           LWD_USER=lightwalletd
ARG           LWD_UID=2002

RUN           useradd --home-dir /srv/$LWD_USER \
                --shell /bin/bash \
                --create-home \
                --uid $LWD_UID\
                    $LWD_USER
USER          $LWD_USER
WORKDIR       /srv/$LWD_USER

COPY          ./lightwalletd_zcash.conf /srv/lightwalletd/.zcash/zcash.conf
CMD           [ "/usr/local/bin/lightwalletd", \
                "--log-level", "7", \
                "--grpc-bind-addr", "0.0.0.0:9067", \
                "--http-bind-addr", "0.0.0.0:9068", \
                "--no-tls-very-insecure", \
                "--zcash-conf-path", "/srv/lightwalletd/.zcash/zcash.conf", \
                "--data-dir", ".", \
                "--log-file", "/dev/stdout" ]
