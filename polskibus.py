#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Polskibus.
Usage:
	polskibus.py list [<city>]
	polskibus.py check <city> <date> [--pax=PAX --promo=PROMO --max-days=MAX (-e CITY)...]
"""
import sys
import requests
import datetime
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
		if not self.cookies:
			self.cookies = r.cookies

	def get_destinations(self, destination):
		r = requests.get('http://www.polskibus.com/polskibus/origin/{}'.format(self.origins[destination]), cookies=self.cookies)
		if not self.cookies:
			self.cookies = r.cookies
		o = requests.get('http://www.polskibus.com/polskibus/destinations', cookies=self.cookies)
		if o.status_code != 200:
			raise RuntimeError("Some stupid error during retrieving destinations occurred.")
		soup = Soup(o.text)
		for city in soup.findAll('option')[1:]:
			self.destinations[city.text.encode('utf-8')] = city['value']

	def set_destination(self, destination_id):
		requests.get("http://www.polskibus.com/polskibus/destination/{}".format(destination_id))

	def set_outbound(self, date):
		r = requests.get('http://www.polskibus.com/polskibus/outbound/{}'.format(date), cookies=self.cookies)
		if r.status_code != 200: 
			raise RuntimeError('Value "{}" is invalid or connection problem to polskibus.com page.')
		requests.get('http://www.polskibus.com/polskibus/return/1')

	def set_return(self, date):
		r = requests.get('http://www.polskibus.com/polskibus/return/{}'.format(date), cookies=self.cookies)
		if r.status_code != 200:
			raise RuntimeError('Value "{}" may be invalid or just stupid.'.format(date))

	def get_routes(self):
		r = requests.get('http://www.polskibus.com/search-results', cookies=self.cookies)



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
		outbound_date = datetime.datetime.strptime(args['<date>'],'%d/%m/%Y')

		max_days = int(args['--max-days'] or 31)
		for destination in polskibus.destinations:
			polskibus.set_destination(destination)
			for outbound_shift in range(0, max_days):
				outbound_date = outbound_date + datetime.timedelta(days=outbound_shift)
				polskibus.set_outbound(outbound_date.strftime('%d/%m/%Y'))
				for return_shift in range(1, max_days - outbound_shift):
					return_date = outbound_date + datetime.timedelta(days=return_shift)
					polskibus.set_return(return_date.strftime('%d/%m/%Y'))



