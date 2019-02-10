#!/usr/bin/python
from json import loads
from time import strptime, strftime
from sys import exit
import requests
from sys import argv
import argparse as ap

#Set up arguments to program
parser = ap.ArgumentParser(description="Delete tags from a docker trusted registry using REST API.")

parser.add_argument('-n', '--noop', action='store_true', help='Show a count of tags that are expected to be deleted and kept, then exit')
parser.add_argument('-k', '--keep', type=int, help='Number of newest tags to keep', default=25)
parser.add_argument('-b', '--baseurl',  help='Base url to the registry, including protocol. Default: "https://dtr.nrk.no"', 
	default='https://dtr.nrk.no')
parser.add_argument('-r', '--repo', help='The repository you want to perform operations on - Ex: origo/folkemusikk', required=True)
parser.add_argument('-u', '--user', help='Username to authenticate as', required=True)
parser.add_argument('-t', '--token', help='Authentication token. Must be created in the registry.', required=True)
parser.add_argument('-i', '--ignore', help='Tag to ignore/keep. Can be specified multiple times.', action='append')

args = parser.parse_args()

baseurl = "%s/api/v0" % args.baseurl
timeformat = "%Y-%m-%dT%H:%M:%S"

class TagData:
    
    def __init__(self, jsondata):
        self.name = jsondata['name']
        self.digest = jsondata['digest']
        self.createdstr = jsondata['createdAt']
        self.created = strptime(jsondata['createdAt'].split('.')[0], timeformat)

    def delete(self):
        if self.name not in args.ignore and not args.noop:
            print "Deleting tag %s from %s" % (self.name, args.repo)
            d = requests.delete("%s/repositories/%s/tags/%s" % (baseurl, args.repo, self.name), auth=(args.user, args.token))
            return d.status_code == 200
        else:
            print "Skipping tag %s from %s" % (self.name, args.repo)
            return False

    def __str__(self):
        return str("%s: %s, %s" % (self.name, self.digest, self.createdstr))

    def __cmp__(self, other):
	return cmp(self.created, other.created)

class Controller:

    def __init__(self, keep):
        tagreq = requests.get("%s/repositories/%s/tags?pageSize=100000" % (baseurl, args.repo), auth=(args.user, args.token))
        tagdata = tagreq.json()
        self.tags = sorted(map(lambda t: TagData(t),  tagdata))
        self.tokeep = self.tags[-keep:]
	self.todelete = self.tags[:-min(len(self.tags), keep)]

    def dump(self):
        for t in self.tags: print t

    def info(self):
        print "Will delete %s oldest tags, and keep latest %s tags" % (len(self.todelete), len(self.tokeep))

    def delete(self):
        for t in self.todelete: t.delete()

if __name__ == '__main__':
    c = Controller(args.keep)
    c.info()
    c.delete()
