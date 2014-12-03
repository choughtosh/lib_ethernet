#!/usr/bin/env python
import xmostest
import os
import random
from mii_clock import Clock
from mii_phy import MiiTransmitter
from rgmii_phy import RgmiiTransmitter
from mii_packet import MiiPacket
from helpers import do_rx_test


def do_test(impl):
    resources = xmostest.request_resource("xsim")

    binary = 'test_etype_filter/bin/%s/test_etype_filter_%s.xe' % (impl, impl)

    dut_mac_address = [0,1,2,3,4,5]
    packets = [
        MiiPacket(dst_mac_addr=dut_mac_address, src_mac_addr=[0 for x in range(6)],
                  ether_len_type=[0x11, 0x11], data_bytes=[1,2,3,4] + [0 for x in range(50)]),
        MiiPacket(dst_mac_addr=dut_mac_address, src_mac_addr=[0 for x in range(6)],
                  ether_len_type=[0x22, 0x22], data_bytes=[5,6,7,8] + [0 for x in range(60)])
      ]

    clock_25 = Clock('tile[0]:XS1_PORT_1J', Clock.CLK_25MHz)
    phy = MiiTransmitter('tile[0]:XS1_PORT_1A',
                         'tile[0]:XS1_PORT_4E',
                         'tile[0]:XS1_PORT_1K',
                         clock_25,
                         verbose=True)

    phy.set_packets(packets)
    
    tester = xmostest.pass_if_matches(open('test_etype_filter.expect'),
                                     'lib_ethernet', 'basic_tests',
                                      'etype_filter_test', {'impl':impl})

    xmostest.run_on_simulator(resources['xsim'], binary,
                              simthreads = [clock_25, phy],
                              tester = tester)


def runtest():
    random.seed(1)
    
    do_test("standard")
    do_test("rt")