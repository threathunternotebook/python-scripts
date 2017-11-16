#!/bin/python
from optparse import *
import sys
import os

# Create a yaml file of blacklisted md5s to use with logstash's translate plugin
# Allows you to track bad md5s using elastic stack
def main(infile):
  outfile = "blacklisted_md5.txt"
  md5List = []
  buffer = ""
  linenum = 0

  #open md5 file for reading
  md5file = open(infile, 'r').readlines()
  for line in md5file:
      md5List.append(line.rstrip().lower())
      buffer += '"' + md5List[linenum] + '": ' + '"true"' +'\n'
      linenum += 1
  md5outfile = open(outfile, 'w')
  md5outfile.writelines(buffer)
  md5outfile.close()
  # Completed yaml file will be written to current directory
  cmd = "sort -u " + outfile + " > " + "blacklisted_md5.yaml"
  os.system(cmd)
  cmd1 = "rm -f " + outfile
  os.system(cmd1)

if __name__ == "__main__":
   # Supply a text file of md5 hashes where there is one hash per line
   parser = OptionParser()
   parser.add_option("-f", "--file", action="store_true", dest="file", help="file containing list of md5s", default="md5list.txt")

   (options, args) = parser.parse_args()
   if len(args) != 1:
     print "please use all arguments"
     sys.exit()
   infile = args[0]
   print "The argument passed to main is: " + infile 

   main(infile)

