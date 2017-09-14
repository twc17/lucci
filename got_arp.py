#!/usr/bin/python

# Author: Troy W. Caro <twc17@pitt.edu>
# Date: Sep 14, 2017
# Version: 1.0.0
#
# Purpose:
#   This script will log in to a list of routers and grab the ARP table
#
# Dependencies:
#   python 2.6+
#   netmiko
#
# Usage:
#   python got_arp.py ROUTER_LIST 

# Imports
import os
import sys
import time
import argparse
import netmiko


parser = argparse.ArgumentParser(description='Gather number of ARP entries for each VLAN')
parser.add_argument('input_router_file', metavar='FILE', help="Text file conntaining the FQDN router list")
args = parser.parse_args()

router_file = open(args.input_router_file, 'r')



