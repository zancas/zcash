#!/usr/bin/env python
# Copyright (c) 2014 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Test -reindex with CheckBlockIndex
#

import sys; assert sys.version_info < (3,), ur"This script does not run under Python 3. Please use Python 2.7.x."
import os, shutil

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, initialize_datadir, \
    start_node, stop_node, wait_bitcoinds


# Use the the TestFramework for a consistent interface the runner/reporter.
class ColdCLITest(BitcoinTestFramework):

    def __init__(self):
        self._initialize_test_configuration()

    def _initialize_test_configuration(self):
        datadir = initialize_datadir("cache", 0) # Overwrite port/rpcport in zcash.conf
        self.options, self.args = self.parse_options_args() 
        self.nodes = [start_node(0, self.options.tmpdir)]
        from_dir = os.path.join("cache", "node0")
        to_dir = os.path.join(self.options.tmpdir,  "node0")
        print("from_dir: %s :: to_dir: %s" % (from_dir, to_dir))
        shutil.copytree(from_dir, to_dir)

    def setup_chain(self):
        pass#initialize_chain_clean(self.options.tmpdir, 1)

    def setup_network(self):
        pass
        
    def run_test(self):
        pass

if __name__ == '__main__':
    ColdCLITest().main()
