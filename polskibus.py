#!/usr/bin/env python
"""Polskibus.
Usage:
	polskibus.py list
	polskibus.py check <source> <date> [((-)<city>)...]
"""
import sys
import requests
from BeautifulSoup import BeautifulSoup as Soup
from docopt import docopt

if __name__ == '__main__':
	args = docopt(__doc__, version='Polskibus cos tam 0.1')

	if args['list']:
		r = requests.get('http://www.polskibus.com/bus-stops')
		soup = Soup(r.text)
		print "Available cities:"
		for city in soup.findAll(id='edit-outbound')[0].findAll('option')[1:]:
			print city.text
