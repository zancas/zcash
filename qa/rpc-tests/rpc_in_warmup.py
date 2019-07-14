#!/usr/bin/env python
# Copyright (c) 2014 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Test -reindex with CheckBlockIndex
#

import sys; assert sys.version_info < (3,), \
    ur"This script does not run under Python 3. Please use Python 2.7.x."
import os
import shutil
import subprocess
import time

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, initialize_datadir, rpc_port
from test_framework.authproxy import AuthServiceProxy, JSONRPCException


# Use the the TestFramework for a consistent interface the runner/reporter.
class ColdCLITest(BitcoinTestFramework):

    def __init__(self):
        self._initialize_test_configuration()
        args = [os.getenv("BITCOIND", "bitcoind"),
                "-keypool=1000",
                "-datadir="+self.datadir,
                "-discover=0"]
        self.bitcoind_process = subprocess.Popen(args)
        url = "http://rt:rt@%s:%d" % ('127.0.0.1', rpc_port(0))
        self.nodes = [AuthServiceProxy(url)]

    def _initialize_test_configuration(self):
        self.datadir = initialize_datadir("cache", 0)
        self.options, self.args = self.parse_options_args()
        from_dir = os.path.join("cache", "node0")
        to_dir = os.path.join(self.options.tmpdir,  "node0")
        shutil.copytree(from_dir, to_dir)

    def setup_chain(self):
        pass

    def setup_network(self):
        pass

    def run_test(self):
        time.sleep(3)
        try:
            self.nodes[0].z_sendmany()
        except JSONRPCException as e:
            assert_equal(-28, e.error['code'])

        assert_equal([], self.nodes[0].z_listaddresses())

        try:
            self.nodes[0].z_sendmany()
        except JSONRPCException as e:
            assert_equal(-28, e.error['code'])


if __name__ == '__main__':
    ColdCLITest().main()
