#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Polskibus.
Usage:
	polskibus.py list [<city>]
	polskibus.py check <city> <date> [--pax=PAX --promo=PROMO --max-days=MAX (-e CITY)...]
"""
import sys
import requests
from BeautifulSoup import BeautifulSoup as Soup
from docopt import docopt

class Polskibus:
	def __init__(self):
		self.origins = dict()
		self.destinations = dict()
		self.cookies = None
		pass

	def get_origins(self):
		r = requests.get('http://www.polskibus.com/polskibus/origins')
		soup = Soup(r.text)
		for city in soup.findAll('option')[1:]:
			self.origins[city.text] = city['value']

	def get_destinations(self, destination):
		r = requests.get('http://www.polskibus.com/polskibus/origin/{}'.format(self.origins[destination]))
		if not self.cookies:
			self.cookies = r.cookies
		o = requests.get('http://www.polskibus.com/polskibus/destinations', cookies=self.cookies)
		soup = Soup(o.text)
		for city in soup.findAll('option')[1:]:
			self.destinations[city.text] = city['value']

	def set_destination(self, destination_id):
		requests.get("http://www.polskibus.com/polskibus/destination/{}".format(destination_id))

	def set_outbound(self, date):
		if requests.get('http://www.polskibus.com/polskibus/outbound/{}'.format(date), cookies=self.cookies).status_code != 200:
			raise RuntimeError('Value "{}" is invalid or connection problem to polskibus.com page.')
		requests.get('http://www.polskibus.com/polskibus/return/1')


if __name__ == '__main__':
	args = docopt(__doc__, version='Polskibus cos tam 0.1')

	polskibus = Polskibus()
	polskibus.get_origins()
	if args['list']:
		if not args['<city>']:
			print "Available cities:"
			for city in polskibus.origins:
				print city
		else:
			print "Destination cities available for {}:".format(args['<city>'])
			# for city in polskibus.get_destinations(args['<city>'][0]):
			polskibus.get_destinations(args['<city>'].decode('utf-8'))
			for city in polskibus.destinations:
				print city
	elif args['check']:
		polskibus.get_destinations(args['<city>'].decode('utf-8'))		
		for e in args['CITY']:
			try:
				del polskibus.destinations[e]
			except KeyError:
				pass
		polskibus.set_outbound(args['<date>'])


