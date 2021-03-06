#!/usr/bin/python

# Author: Troy W. Caro <twc17@pitt.edu>
# Date: Sep 8, 2017 
# Version: 1.1.1
#
# Purpose:
#   This script uses the output file generated from vlan_usage_via_arp_entries.pl
#   It will then output all of the VLANs with 2 or less entries in the ARP table
#
# Dependencies:
#   python version 2.6+
#
# Usage:
#   python ununsed_vlans.py FILE_OF_ARP_ENTRIES

# Imports
import os
import sys
import argparse
import smtplib

# Packages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
fromaddr = "unused_vlans@tsunami.ns.pitt.edu"
toaddr = "twc17@pitt.edu"

msg = MIMEMultipart()
msg['Subject'] = "Unused VLANs"
msg['From'] = fromaddr
msg['To'] = toaddr

body = "Attached is a list of VLANs that have less than two entries in the ARP table"

msg.attach(MIMEText(body, 'plain'))

filename = "unused_vlans.txt"
attachment = open("unused_vlans.txt", 'rb')

part = MIMEText(attachment.read())
part.add_header('Content-Disposition', "attachment", filename=filename)
 
msg.attach(part)

server = smtplib.SMTP('smtp.pitt.edu', 25)
text = msg.as_string()

# Try to send it!
try:
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
except Exception as e:
        print(e)
attachment.close()
