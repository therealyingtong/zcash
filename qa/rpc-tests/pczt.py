#!/usr/bin/env python3
# Copyright (c) 2020 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php .

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_equal,
    bytes_to_hex_str,
    hex_str_to_bytes,
    initialize_chain,
    start_nodes,
    get_coinbase_address,
    wait_and_assert_operationid_status,
)
from decimal import Decimal
import json

class PcztTest(BitcoinTestFramework):

    def setup_chain(self):
        print("Initializing test directory "+self.options.tmpdir)
        initialize_chain(self.options.tmpdir)

    def setup_nodes(self):
        return start_nodes(4, self.options.tmpdir)

    def run_test(self):

        # We can construct a PCZT without p2p connection
        self.split_network()

        # Shield coinbase on Node 0
        zaddr0 = self.nodes[0].z_getnewaddress('sapling')
        coinbase0 = get_coinbase_address(self.nodes[0])
        opid = self.nodes[0].z_shieldcoinbase("*", zaddr0)['opid']
        txid = wait_and_assert_operationid_status(self.nodes[0], opid)
        self.nodes[0].generate(1)
        self.sync_all()
        print(self.nodes[0].z_getbalance(zaddr0))

        # Create generic pczt on Node 2
        pczt = self.nodes[2].createpczt()
        print(pczt)

        # We intend to send outputs to Nodes 2 and 3
        zaddr2 = self.nodes[2].z_getnewaddress('sapling')
        pczt_object = self.nodes[2].pczt_addoutput(pczt, zaddr2, Decimal('1'))
        # print(pczt_object['pczt'])

        zaddr3 = self.nodes[3].z_getnewaddress('sapling')
        pczt_object = self.nodes[3].pczt_addoutput(pczt_object['pczt'], zaddr3, Decimal('1'))
        # print(pczt_object['pczt'])

        # We fund the outputs with spends from zaddr0
        pczt_object = self.nodes[0].pczt_fund(pczt_object['pczt'], zaddr0)
        # print(pczt_object['pczt'])

        # Print out the pczt so far
        decoded_pczt = self.nodes[0].decodepczt(pczt_object['pczt'])
        print(json.dumps(decoded_pczt, indent=4))

        # Finalize the spends
        raw_tx_hex = self.nodes[0].finalizepczt(pczt_object['pczt'])
        print(raw_tx_hex)

if __name__ == '__main__':
    PcztTest().main()