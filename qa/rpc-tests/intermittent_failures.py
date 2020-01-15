#!/usr/bin/env python
# Copyright (c) 2018 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php .

import sys; assert sys.version_info < (3,), ur"This script does not run under Python 3. Please use Python 2.7.x."

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_equal,
    get_coinbase_address,
    wait_and_assert_operationid_status,
)

from decimal import Decimal
from pprint import pprint as pp
import time

# Test wallet z_listunspent behaviour across network upgrades
class WalletListNotes(BitcoinTestFramework):

    def _send_amt(self, from_addr, to_addr, amnt):
        recipients = [{"address": to_addr, "amount": amnt}]
        myopid = self.nodes[0].z_sendmany(from_addr, recipients)
        return wait_and_assert_operationid_status(self.nodes[0], myopid)

    def run_test(self):
        receive_amount_10 = Decimal('10.0') - Decimal('0.0001')
        # Send 9.9999 ZEC to a z-addr
        saplingzaddr = self.nodes[0].z_getnewaddress('sapling')
        txid_1 = self._send_amt(get_coinbase_address(self.nodes[0]), saplingzaddr, receive_amount_10)

        start = time.time()
        while self.nodes[0].z_listunspent(0, 9999, False, [saplingzaddr]) == []:
            time.sleep(0.01)
        stop = time.time()
        print(stop - start)

if __name__ == '__main__':
    WalletListNotes().main()
