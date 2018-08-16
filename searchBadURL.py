# Python Script to Query URLS/Web Hosts

from elasticsearch import Elasticsearch
from optparse import OptionParser

def main():
   parser = OptionParser(usage="usage: %prog [options] filename", version="%prog 0.1")
   parser.add_option("-f", "--file", dest="file",  help="file with malicious URLs to scan")
   parser.add_option("-e", "--ehost", dest="host", default="127.0.0.1", help="Elasticsearch host IP address")
   parser.add_option("-p", "--port", dest="port",  default="9200", help="Elasticsearch host port")
   parser.add_option("-i", "--index", dest="index", help="Elasticsearch index to query")
   (options, args) = parser.parse_args()
  
   if options.file is None:
     print "Must supply filename"
     parser.print_help()
     exit(-1)

   if options.index is None:
     print "Must supply index name"
     parser.print_help()
     exit(-1)

   es = Elasticsearch([options.host], port=options.port)
   bad_urls = open(options.file, "r")

   print "\n\nSearching for bad URLs in Bro HTTP logs"
   for url in bad_urls.readlines():
      res = es.search(index=options.index, doc_type="_doc", body={"query": { "term": {"uri": str(url.strip('\n'))}}})
      print url
      print("%d documents found" % res['hits']['total'])
      print "Bro Log\t\tSource IP\tDestination IP\t\t\t\t\t\t\tIndex"
      for doc in res['hits']['hits']:
         print "%s\t%s\t%s\t\t\t\t\t\t\t%s" % (str(doc ["_type"]), str(doc ['_source']['id.orig_h']), str(doc ['_source']['id.resp_h']), str(doc ['_index']))
   bad_urls.close()

   bad_query = open(options.file, "r")
   print "\n\nSearching for bad URL queries in Bro DNS logs"
   for url in bad_query.readlines():
      res = es.search(index=options.index, doc_type="_doc", body={"query": { "match": {"term": str(url.strip('\n'))}}})
      print url
      print("%d documents found" % res['hits']['total'])
      print "Bro Log\t\tSource IP\tDestination IP\t\t\t\t\t\t\tIndex"
      for doc in res['hits']['hits']:
         print "%s\t%s\t%s\t\t\t\t\t\t\t%s" % (str(doc ["_type"]), str(doc ['_source']['id.orig_h']), str(doc ['_source']['id.resp_h']), str(doc ['_index']))

   bad_query.close()

if __name__ == '__main__':
   main()

