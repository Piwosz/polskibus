#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Polskibus.
Usage:
	polskibus.py list [<city>]
	polskibus.py check <source> <date> [--promo=<promo> --max-days=<max-days> ((-)<city>)...]
"""
import sys
import requests
from BeautifulSoup import BeautifulSoup as Soup
from docopt import docopt

class Polskibus:
	def __init__(self):
		self.origins = dict()
		pass

	def get_origins(self):
		r = requests.get('http://www.polskibus.com/polskibus/origins')
		soup = Soup(r.text)
		for city in soup.findAll('option')[1:]:
			self.origins[city.text] = city['value']

	def get_destinations(self, destination):
		r = requests.get('http://www.polskibus.com/polskibus/destination/{}'.format(self.origins[destination]))
		o = requests.get('http://www.polskibus.com/polskibus/destinations', cookies=r.cookies)
		return o

if __name__ == '__main__':
	args = docopt(__doc__, version='Polskibus cos tam 0.1')

	if args['list']:
		polskibus = Polskibus()
		polskibus.get_origins()
		if not args['<city>']:
			print "Available cities:"
			for city in polskibus.origins:
				print city
		else:
			print "Destination cities available for {}".format(args['<city>'][0])
			for city in polskibus.get_destinations(args['<city>'][0]):
				pass


	elif args['check']:
		print args
		print "-----------------------------------------------------------------------------"