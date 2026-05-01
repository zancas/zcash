// Copyright (c) 2026 The Zingolabs developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or https://www.opensource.org/licenses/mit-license.php .

#include "chainparams.h"
#include "consensus/consensus.h"
#include "consensus/params.h"
#include "main.h"
#include "test/test_bitcoin.h"
#include "util/system.h"

#include <stdexcept>

#include <boost/test/unit_test.hpp>

// Compile-time invariants. The runtime override at -regtestcoinbasematurity
// is only safe because COINBASE_MATURITY (and the constants derived from it)
// stay at their upstream values; if any of these changes, the override
// bounds and the wallet witness cache horizon need to be re-examined.
static_assert(COINBASE_MATURITY == 100,
    "COINBASE_MATURITY must remain 100; runtime override range depends on it.");
static_assert(MAX_REORG_LENGTH == COINBASE_MATURITY - 1,
    "MAX_REORG_LENGTH must remain COINBASE_MATURITY - 1; wallet WITNESS_CACHE_SIZE is derived from it.");
static_assert(MAX_REORG_LENGTH > 0,
    "MAX_REORG_LENGTH must remain positive (mirrors the static_assert in main.cpp).");

namespace {

// Restores regtest coinbase maturity to its prior value at scope exit, so a
// failing or aborting test case does not leak overridden state into later
// tests. regTestParams is a file-scope singleton in chainparams.cpp; the
// only public way to reset it is to re-run SelectParams with the desired
// value in mapArgs.
struct RegtestMaturityGuard {
    int saved;
    RegtestMaturityGuard()
        : saved(Params(CBaseChainParams::REGTEST).GetConsensus().nCoinbaseMaturity) {}
    ~RegtestMaturityGuard() {
        mapArgs["-regtestcoinbasematurity"] = std::to_string(saved);
        try { SelectParams(CBaseChainParams::REGTEST); } catch (...) {}
        mapArgs.erase("-regtestcoinbasematurity");
    }
};

} // anonymous namespace

BOOST_FIXTURE_TEST_SUITE(coinbase_maturity_tests, BasicTestingSetup)

BOOST_AUTO_TEST_CASE(default_value_matches_constant)
{
    BOOST_CHECK_EQUAL(
        Params(CBaseChainParams::MAIN).GetConsensus().nCoinbaseMaturity,
        COINBASE_MATURITY);
    BOOST_CHECK_EQUAL(
        Params(CBaseChainParams::TESTNET).GetConsensus().nCoinbaseMaturity,
        COINBASE_MATURITY);
}

BOOST_AUTO_TEST_CASE(regtest_override_applies)
{
    RegtestMaturityGuard guard;
    mapArgs["-regtestcoinbasematurity"] = "5";
    BOOST_CHECK_NO_THROW(SelectParams(CBaseChainParams::REGTEST));
    BOOST_CHECK_EQUAL(
        Params(CBaseChainParams::REGTEST).GetConsensus().nCoinbaseMaturity, 5);
    mapArgs.erase("-regtestcoinbasematurity");
}

BOOST_AUTO_TEST_CASE(boundary_values_accepted)
{
    RegtestMaturityGuard guard;

    mapArgs["-regtestcoinbasematurity"] = "1";
    BOOST_CHECK_NO_THROW(SelectParams(CBaseChainParams::REGTEST));
    BOOST_CHECK_EQUAL(
        Params(CBaseChainParams::REGTEST).GetConsensus().nCoinbaseMaturity, 1);

    mapArgs["-regtestcoinbasematurity"] = std::to_string(COINBASE_MATURITY);
    BOOST_CHECK_NO_THROW(SelectParams(CBaseChainParams::REGTEST));
    BOOST_CHECK_EQUAL(
        Params(CBaseChainParams::REGTEST).GetConsensus().nCoinbaseMaturity,
        COINBASE_MATURITY);

    mapArgs.erase("-regtestcoinbasematurity");
}

BOOST_AUTO_TEST_CASE(rejects_zero)
{
    RegtestMaturityGuard guard;
    mapArgs["-regtestcoinbasematurity"] = "0";
    BOOST_CHECK_THROW(SelectParams(CBaseChainParams::REGTEST), std::runtime_error);
    mapArgs.erase("-regtestcoinbasematurity");
}

BOOST_AUTO_TEST_CASE(rejects_negative)
{
    RegtestMaturityGuard guard;
    mapArgs["-regtestcoinbasematurity"] = "-3";
    BOOST_CHECK_THROW(SelectParams(CBaseChainParams::REGTEST), std::runtime_error);
    mapArgs.erase("-regtestcoinbasematurity");
}

BOOST_AUTO_TEST_CASE(rejects_above_max)
{
    RegtestMaturityGuard guard;
    mapArgs["-regtestcoinbasematurity"] = std::to_string(COINBASE_MATURITY + 1);
    BOOST_CHECK_THROW(SelectParams(CBaseChainParams::REGTEST), std::runtime_error);
    mapArgs.erase("-regtestcoinbasematurity");
}

BOOST_AUTO_TEST_CASE(rejects_unparseable)
{
    RegtestMaturityGuard guard;

    for (const auto& bad : { std::string("abc"),
                              std::string("1.5"),
                              std::string("5abc"),
                              std::string("") }) {
        mapArgs["-regtestcoinbasematurity"] = bad;
        BOOST_CHECK_THROW(
            SelectParams(CBaseChainParams::REGTEST), std::runtime_error);
    }

    mapArgs.erase("-regtestcoinbasematurity");
}

BOOST_AUTO_TEST_CASE(non_regtest_does_not_apply_override)
{
    // SelectParams must not mutate mainnet/testnet params even if the flag
    // happens to be present in mapArgs. (init.cpp returns InitError before
    // we get here in normal startup; this guards the chainparams layer.)
    mapArgs["-regtestcoinbasematurity"] = "5";

    BOOST_CHECK_NO_THROW(SelectParams(CBaseChainParams::MAIN));
    BOOST_CHECK_EQUAL(
        Params(CBaseChainParams::MAIN).GetConsensus().nCoinbaseMaturity,
        COINBASE_MATURITY);

    BOOST_CHECK_NO_THROW(SelectParams(CBaseChainParams::TESTNET));
    BOOST_CHECK_EQUAL(
        Params(CBaseChainParams::TESTNET).GetConsensus().nCoinbaseMaturity,
        COINBASE_MATURITY);

    mapArgs.erase("-regtestcoinbasematurity");
    SelectParams(CBaseChainParams::REGTEST); // restore default chain
}

BOOST_AUTO_TEST_SUITE_END()
