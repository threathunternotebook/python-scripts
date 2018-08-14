#!/bin/python
from optparse import *
import sys
import os

# Create yaml file of blacklisted IP addresses to use with logstash's translate plugin
# Allows you to track bad ip addresses using elastic stack
def main(infile):
  outfile = "blacklisted_ip.txt"
  ipList = []
  buffer = ""
  linenum = 0

  #open ip file for reading
  ipfile = open(infile, 'r').readlines()
  for line in ipfile:
      ipList.append(line.rstrip())
      buffer += '"' + ipList[linenum] + '": ' + '"true"' +'\n'
      linenum += 1
  ipoutfile = open(outfile, 'w')
  ipoutfile.writelines(buffer)
  ipoutfile.close()
  # Completed yaml file will be written to current directory
  cmd = "sort -u " + outfile + " > " + "blacklisted_ip.yaml"
  os.system(cmd)
  cmd1 = "rm -f " + outfile
  os.system(cmd1)

if __name__ == "__main__":
   # Supply a text file of bad IP addresses where there is one IP address per line
   parser = OptionParser()
   parser.add_option("-f", "--file", action="store_true", dest="file", help="file containing list of ip addresses", default="iplist.txt")

   (options, args) = parser.parse_args()
   if len(args) != 1:
     print "please use all arguments"
     sys.exit()
   infile = args[0]
   print "The argument passed to main is: " + infile 

   main(infile)

