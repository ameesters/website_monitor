#!/usr/bin/env python
import os, time, httplib
from termcolor import colored

SITES = [
	"www.clubseventeen.com",
	"www.jimslip.com",
	"www.seventeenlive.com",
	"www.packofporn.com",
	"www.glossyangels.com",
	"www.clubsweethearts.com",
	"www.fun.nl",
	"www.imco.nl",
	"www.sniffmytuna.com",
	"www.aboutbigboobs.com",
	"www.analpetite.com",
	"www.analslurp.com",
	"www.analstretched.com",
	"www.beautyandthesenior.com",
	"www.beautyandthesenior.tv",
	"www.clubsweethearts.nl",
	"www.creamedonglasses.com",
	"www.hairytokyoteens.com",
	"www.holeyfuck.com",
	"www.hornylilnymphs.com",
	"www.jerkandslurp.com",
	"www.laralatex.com",
	"www.larasplayground.com",
	"www.lesbiankinkdom.com",
	"www.mysecrettime.com",
	"www.mysexykittens.com",
	"www.peeinggames.com",
	"www.publicplacepussy.com",
	"www.redlightsextrips.com",
	"www.retroraw.com",
	"www.rimbledon.com",
	"www.rodox.com",
	"www.seventeenvideo.com",
	"www.sleepsurprise.com",
	"www.spunkyteens.com",
	"www.teenagegroupsex.com",
	"www.teensex.nl",
	"www.teensexsecrets.com",
	"www.teensfromtokyo.com",
	"www.tokyogroupsex.com",
	"www.ukroadtrips.com",
	"www.vintageclassicporn.com",
	"www.youngbusty.com"
]

while 1:
	for site in SITES:
		conn = httplib.HTTPConnection(site, timeout=10)
		conn.request("HEAD", "/")
		response = conn.getresponse()
		
		if response.status not in (200, 301):
			print "\a"
			response.status = colored(response.status, 'red')
					
		print "{0:30} {1:10} {2:10}".format(site, response.status, response.reason)
		conn.close()
	
	time.sleep(2)
	os.system("clear")
