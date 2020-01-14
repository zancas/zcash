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

# Test wallet z_listunspent behaviour across network upgrades
class WalletListNotes(BitcoinTestFramework):

    def run_test(self):
        # Current height = 200
        assert_equal(200, self.nodes[0].getblockcount())

        # Get some ZEC at a z-addr
        saplingzaddr = self.nodes[0].z_getnewaddress('sapling')
        receive_amount_10 = Decimal('10.0') - Decimal('0.0001')
        recipients = [{"address":saplingzaddr, "amount": receive_amount_10}]
        myopid = self.nodes[0].z_sendmany(get_coinbase_address(self.nodes[0]), recipients)

        # Send 1.0 (actually 0.9999) from saplingzaddr to a new zaddr
        receive_amount_point_1 = Decimal('0.1') - Decimal('0.0001')
        change_amount_9 = receive_amount_10 - Decimal('0.1')
        assert_equal('sapling', self.nodes[0].z_validateaddress(saplingzaddr)['type'])
        saplingzaddr2 = self.nodes[0].z_getnewaddress('sapling')
        assert_equal('sapling', self.nodes[0].z_validateaddress(saplingzaddr2)['type'])
        recipients = [{"address": saplingzaddr2, "amount":receive_amount_point_1}]
        myopid = self.nodes[0].z_sendmany(saplingzaddr, recipients)
        txid_2 = wait_and_assert_operationid_status(self.nodes[0], myopid)
        
        # list unspent, allowing 0conf txs
        unspent_tx = self.nodes[0].z_listunspent(0)
        breakpoint()
        assert_equal(len(unspent_tx), 2)

if __name__ == '__main__':
    WalletListNotes().main()