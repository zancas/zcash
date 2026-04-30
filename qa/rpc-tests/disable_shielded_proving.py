#!/usr/bin/env python3
# Copyright (c) 2026 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php .

"""Exercise the -disableshieldedproving CLI flag.

Coverage:
- Node startup with -disableshieldedproving and a transparent
  -mineraddress succeeds, and the debug log records that proving-key
  load was skipped.
- Transparent mining still works.
- z_sendmany, z_shieldcoinbase, and z_mergetoaddress are rejected with
  the dedicated error message.
- Node startup with -disableshieldedproving and a shielded
  -mineraddress is refused at arg-parse time.
"""

from test_framework.authproxy import JSONRPCException
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    SAPLING_BRANCH_ID,
    assert_equal,
    assert_raises_message,
    assert_start_raises_init_error,
    nuparams,
    start_node,
    stop_node,
)


# Known regtest addresses used only as -mineraddress targets. They are
# never spent from in this test.
TRANSPARENT_MINER_TADDR = "tmDjbRj8go7BrS8AxSjfjTBsCcHw7J45SCi"
SAPLING_MINER_ZADDR = (
    "zregtestsapling1ssqj3f3majnl270985gqcdqedd9t4nlttjqskccwevj2v20sc25"
    "deqspv3masufnwcdy67cydyy"
)

REJECTION_MSG = "is unavailable because zcashd was started with -disableshieldedproving"
STARTUP_REFUSE_MSG = "incompatible with -disableshieldedproving"
SKIP_LOG_LINE = "skipping Sapling/Orchard proving-key load"


class DisableShieldedProvingTest(BitcoinTestFramework):

    def __init__(self):
        super().__init__()
        self.num_nodes = 1
        self.cache_behavior = 'clean'

    def setup_network(self, split=False):
        self.nodes = [start_node(0, self.options.tmpdir, self._happy_args())]
        self.is_network_split = False
        self.sync_all()

    def _happy_args(self):
        return [
            '-disableshieldedproving',
            nuparams(SAPLING_BRANCH_ID, 1),
            '-mineraddress=%s' % TRANSPARENT_MINER_TADDR,
            '-minetolocalwallet=0',
        ]

    def run_test(self):
        self._test_startup_log_message()
        self._test_transparent_mining_works()
        self._test_shielded_rpcs_rejected()
        self._test_shielded_mineraddress_refused()

    def _test_startup_log_message(self):
        logpath = self.options.tmpdir + "/node0/regtest/debug.log"
        with open(logpath, "r", encoding="utf8") as f:
            log = f.read()
        assert SKIP_LOG_LINE in log, (
            "expected log line %r not found in debug.log" % SKIP_LOG_LINE)

    def _test_transparent_mining_works(self):
        node = self.nodes[0]
        before = node.getblockcount()
        node.generate(3)
        assert_equal(node.getblockcount(), before + 3)

    def _test_shielded_rpcs_rejected(self):
        node = self.nodes[0]

        recipients = [{"address": TRANSPARENT_MINER_TADDR, "amount": 0.1}]
        assert_raises_message(
            JSONRPCException, REJECTION_MSG,
            node.z_sendmany, "ANY_TADDR", recipients,
        )
        assert_raises_message(
            JSONRPCException, REJECTION_MSG,
            node.z_shieldcoinbase, "ANY_TADDR", SAPLING_MINER_ZADDR,
        )
        assert_raises_message(
            JSONRPCException, REJECTION_MSG,
            node.z_mergetoaddress, ["ANY_TADDR"], SAPLING_MINER_ZADDR,
        )

    def _test_shielded_mineraddress_refused(self):
        # Stop the running node, then attempt to relaunch with a Sapling
        # mineraddress while -disableshieldedproving is on. Should be
        # rejected at startup before any chain state is touched.
        stop_node(self.nodes[0], 0)
        self.nodes = []

        bad_args = [
            '-disableshieldedproving',
            nuparams(SAPLING_BRANCH_ID, 1),
            '-mineraddress=%s' % SAPLING_MINER_ZADDR,
            '-minetolocalwallet=0',
        ]
        assert_start_raises_init_error(
            0, self.options.tmpdir, bad_args,
            expected_msg=STARTUP_REFUSE_MSG,
        )


if __name__ == '__main__':
    DisableShieldedProvingTest().main()
