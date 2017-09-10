#!/usr/bin/python

# Author: Troy W. Caro <twc17@pitt.edu>
# Date: Sep 8, 2017 
# Version: 1.0.0
#
# Purpose:
#   This script uses the output file generated from vlan_usage_via_arp_entries.pl
#   It will then output all of the VLANs with 2 or less entries in the ARP table
#
# Usage:
#   python3 ununsed_vlans.py FILE_OF_ARP_ENTRIES.log
#
# Note:
#   Not using any of the mail stuff yet

# Imports
import os
import sys
import argparse
# import smtplib

parser = argparse.ArgumentParser(description='Extract unused VLANs from ARP entry log file')
parser.add_argument('input_arp_file', metavar='FILE', help="Log file containing number of ARP entries per VLAN") 
args = parser.parse_args()

arp_file = open(args.input_arp_file, 'r')


for line in arp_file:
    line = line.split(',')
    if int(line[-1]) <= 2:                                               
        output = open('unused_vlans.txt', 'a')
        output.write(",".join(line))
        output.close()

arp_file.close()                                                    

# Time to build the email
# msg = MIMEMultipart()
# msg['Subject'] = "Unused VLANs"
# msg['From'] = "nocjob@tsunami.ns.pitt.edu"
# msg['To'] = "pittnet-techs-l@list.pitt.edu"

