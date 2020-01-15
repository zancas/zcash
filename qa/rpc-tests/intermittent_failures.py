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
from time import time

# Test wallet z_listunspent behaviour across network upgrades
class WalletListNotes(BitcoinTestFramework):

    def run_test(self):
        # Current height = 200
        assert_equal(200, self.nodes[0].getblockcount())

        # Get some ZEC at a z-addr
        saplingzaddr = self.nodes[0].z_getnewaddress('sapling')
        receive_amount_10 = Decimal('10.0') - Decimal('0.0001')
        coinbasepayee = [{"address": saplingzaddr, "amount": receive_amount_10}]
        myopid = self.nodes[0].z_sendmany(get_coinbase_address(self.nodes[0]), coinbasepayee)
        txid_1 = wait_and_assert_operationid_status(self.nodes[0], myopid)

        # No funds (with (default) one or more confirmations) in saplingzaddr yet
        assert_equal(0, len(self.nodes[0].z_listunspent()))
        assert_equal(0, len(self.nodes[0].z_listunspent(1)))
        
        # no private balance because no confirmations yet
        assert_equal(0, Decimal(self.nodes[0].z_gettotalbalance()['private']))
        
        # list private unspent, this time allowing 0 confirmations
        unspent_cb = self.nodes[0].z_listunspent(0)
        assert_equal(1, len(unspent_cb))
        assert_equal(False,             unspent_cb[0]['change'])
        assert_equal(txid_1,            unspent_cb[0]['txid'])
        assert_equal(True,              unspent_cb[0]['spendable'])
        assert_equal(saplingzaddr,      unspent_cb[0]['address'])
        assert_equal(receive_amount_10, unspent_cb[0]['amount'])

        # Send 0.001 (actually 0.0009) from saplingzaddr to a new zaddr
        #self.nodes[0].generate(1)
        self.sync_all()
        receive_amount_point_1 = Decimal('0.001') - Decimal('0.0001')
        saplingzaddr2 = self.nodes[0].z_getnewaddress('sapling')
        pp(self.nodes[0].z_listreceivedbyaddress(saplingzaddr))
        recipients = [{"address": saplingzaddr2, "amount": receive_amount_point_1}]
        myopid2 = self.nodes[0].z_sendmany(saplingzaddr, recipients)
        txid_2 = wait_and_assert_operationid_status(self.nodes[0], myopid2)
        pp(self.nodes[0].z_listreceivedbyaddress(saplingzaddr2))
        start = time.time()
        while self.nodes[0].z_listreceivedbyaddress(saplingzaddr2) == []:
            time.sleep(0.1)
        stop = time.time()
        print(stop-start)
        
        '''
        count = 0
        while count < 3:
            count = count + 1
            print("We are inside the %s th iteration of the for loop!" % count)
            print("saplingzaddr: %s" % saplingzaddr)
            myopid = self.nodes[0].z_sendmany(saplingzaddr, recipients)
            txid_2 = wait_and_assert_operationid_status(self.nodes[0], myopid)
        
            # list unspent, allowing 0conf txs
            unspent_tx = self.nodes[0].z_listunspent(0)
            message = "The count at failure was: %s" % count
            print("Before sync the unspent_tx's were: %s" % unspent_tx)
            self.sync_all()
            unspent_tx = self.nodes[0].z_listunspent(0)
            print("After sync unspent_tx's were: %s" % unspent_tx)
            assert_equal(len(unspent_tx), 1 + count, message)
        '''

if __name__ == '__main__':
    WalletListNotes().main()
