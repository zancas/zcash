#!/usr/bin/env python3
# Copyright (c) 2018 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php .


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
        sproutzaddr = self.nodes[0].z_getnewaddress('sprout')
        saplingzaddr = self.nodes[0].z_getnewaddress('sapling')

        # we've got lots of coinbase (taddr) but no shielded funds yet
        assert_equal(0, Decimal(self.nodes[0].z_gettotalbalance()['private']))

        # Set current height to 201
        self.nodes[0].generate(1)
        self.sync_all()
        assert_equal(201, self.nodes[0].getblockcount())

        # Shield coinbase funds (must be a multiple of 10, no change allowed)
        receive_amount_10 = Decimal('10.0') - Decimal('0.0001')
        recipients = [{"address":sproutzaddr, "amount":receive_amount_10}]
        myopid = self.nodes[0].z_sendmany(get_coinbase_address(self.nodes[0]), recipients)
        txid_1 = wait_and_assert_operationid_status(self.nodes[0], myopid)
        print(f"txid_1 is: {txid_1}")
        self.sync_all()
        
        # No funds (with (default) one or more confirmations) in sproutzaddr yet
        assert_equal(0, len(self.nodes[0].z_listunspent()))
        assert_equal(0, len(self.nodes[0].z_listunspent(1)))
        
        # no private balance because no confirmations yet
        assert_equal(0, Decimal(self.nodes[0].z_gettotalbalance()['private']))
        
        # list private unspent, this time allowing 0 confirmations
        unspent_cb = self.nodes[0].z_listunspent(0)
        assert_equal(1, len(unspent_cb))

if __name__ == '__main__':
    WalletListNotes().main()
