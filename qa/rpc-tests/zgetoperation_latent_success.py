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
from pprint import pprint as pp
import time

# Test wallet z_listunspent behaviour across network upgrades
class ZGetOperationResultsLatentSuccess(BitcoinTestFramework):

    def _send_amt(self, from_addr, to_addr, amnt):
        recipients = [{"address": to_addr, "amount": amnt}]
        myopid = self.nodes[0].z_sendmany(from_addr, recipients)
        return wait_and_assert_operationid_status(self.nodes[0], myopid)

    def run_test(self):
        coinbase_addr = get_coinbase_address(self.nodes[0])
        self.nodes[0].generate(10)
        faucet = self.nodes[0].z_getnewaddress('sapling')
        blockreward = Decimal('9.999')
        self._send_amt(coinbase_addr, faucet, blockreward)
        self.nodes[0].generate(10)
        millizec = Decimal('0.001')
        lag_times = []
        for iteration in range(1000):
            print("Iteration: %s" % iteration)
            toaddr = self.nodes[0].z_getnewaddress('sapling')
            self._send_amt(faucet, toaddr, millizec)
            start = time.time()
            while self.nodes[0].z_listunspent(0, 9999, False, [toaddr]) == []:
                time.sleep(0.001)
            stop = time.time()
            lagtime = Decimal(stop) - Decimal(start)
            lag_times.append(lagtime)
            self.nodes[0].generate(10)
            time.sleep(1)
        print(lag_times)
        print(Decimal(sum(lag_times))/Decimal(len(lag_times)))

if __name__ == '__main__':
    ZGetOperationResultsLatentSuccess().main()
