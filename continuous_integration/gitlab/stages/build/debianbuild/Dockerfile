FROM    debian@sha256:903779f30a7ee46937bfb21406f125d5fdace4178074e1cc71c49039ebf7f48f
RUN     apt update && \
        apt install -y build-essential \
                       pkg-config \
                       libc6-dev \
                       m4 \
                       g++-multilib \
                       autoconf \
                       libtool \
                       ncurses-dev \
                       unzip \
                       git \
                       python \
                       python-zmq \
                       python-pip \
                       zlib1g-dev \
                       wget \
                       curl \
                       bsdmainutils \
                       automake              
RUN     pip install pyblake2 pyzmq pyutil python-qpid-proton simplejson
RUN     git clone https://github.com/zcash/zcash.git
WORKDIR /zcash
RUN     ./zcutil/fetch-params.sh --testnet
RUN     ./zcutil/build.sh -j$(nproc)
RUN     mkdir -p /root/.zcash/ && touch /root/.zcash/zcash.conf
