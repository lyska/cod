#!/usr/bin/env python

import sys
from dns.resolver import Resolver, NXDOMAIN, NoNameservers, Timeout, NoAnswer
from threading import Thread

RBLS = [
    '0spam.fusionzero.com',
    'aspews.ext.sorbs.net',
    'b.barracudacentral.org',
    'backscatter.spameatingmonekey.net',
    'bl.deadbeef.com',
    'bl.emailbasura.org',
    'bl.mailspike.net',
    'bl.spamcannibal.org',
    'bl.spamcop.net',
    'blackholes.five-ten-sg.com',
    'blacklist.woody.ch',
    'bogons.cymru.com',
    'cbl.abuseat.org',
    'cdl.anti-spam.org.cn',
    'combined.abuse.ch',
    'combined.rbl.msrbl.net',
    'db.wpbl.info',
    'dnsbl-1.uceprotect.net',
    'dnsbl-2.uceprotect.net',
    'dnsbl-3.uceprotect.net',
    'dnsbl.ahbl.org',
    'dnsbl.cyberlogic.net',
    'dnsbl.dronebl.org',
    'dnsbl.inps.de',
    'dnsbl.njabl.org',
    'dnsbl.rizon.net',
    'dnsbl.sorbs.net',
    'drone.abuse.ch',
    'duinv.aupads.org',
    'dul.dnsbl.sorbs.net',
    'dul.ru',
    'dyna.spamrats.com',
    'dynip.rothen.com',
    'http.dnsbl.sorbs.net'
    'images.rbl.msrbl.net',
    'ips.backscatterer.org',
    'ix.dnsbl.manitu.net',
    'korea.services.net',
    'misc.dnsbl.sorbs.net',
    'noptr.spamrats.com',
    'ohps.dnsbl.net.au',
    'omrs.dnsbl.net.au',
    'orvedb.aupads.org',
    'osps.dnsbl.net.au',
    'osrs.dnsbl.net.au',
    'owfs.dnsbl.net.au',
    'owps.dnsbl.net.au'
    'pbl.spamhaus.org',
    'phishing.rbl.msrbl.net',
    'probes.dnsbl.net.au'
    'proxy.bl.gweep.ca',
    'proxy.block.transip.nl',
    'psbl.surriel.com',
    'rbl.interserver.net',
    'rbl.efnet.org',
    'rdts.dnsbl.net.au',
    'relays.bl.gweep.ca',
    'relays.bl.kundenserver.de',
    'relays.nether.net',
    'residential.block.transip.nl',
    'ricn.dnsbl.net.au',
    'rmst.dnsbl.net.au',
    'sbl.spamhaus.org',
    'short.rbl.jp',
    'smtp.dnsbl.sorbs.net',
    'socks.dnsbl.sorbs.net',
    'spam.abuse.ch',
    'spam.dnsbl.sorbs.net',
    'spam.rbl.msrbl.net',
    'spam.spamrats.com',
    'spamlist.or.kr',
    'spamrbl.imp.ch',
    't3direct.dnsbl.net.au',
    'tor.ahbl.org',
    'tor.dnsbl.sectoor.de',
    'torserver.tor.dnsbl.sectoor.de',
    'ubl.lashback.com',
    'ubl.unsubscore.com',
    'virbl.bit.nl',
    'virus.rbl.jp',
    'virus.rbl.msrbl.net',
    'web.dnsbl.sorbs.net',
    'wormrbl.imp.ch',
    'xbl.spamhaus.org',
    'zen.spamhaus.org',
    'zombie.dnsbl.sorbs.net',
]


class Lookup(Thread):
    def __init__(self, host, dnslist, listed, resolver):
        Thread.__init__(self)
        self.host = host
        self.listed = listed
        self.dnslist = dnslist
        self.resolver = resolver

    def run(self):
        try:
            host_record = self.resolver.query(self.host, "A")
            if len(host_record) > 0:
                self.listed[self.dnslist]['LISTED'] = True
                self.listed[self.dnslist]['HOST'] = host_record[0].address
                text_record = self.resolver.query(self.host, "TXT")
                if len(text_record) > 0:
                    self.listed[self.dnslist]['TEXT'] = "\n".join(text_record[0].strings)
            self.listed[self.dnslist]['ERROR'] = False
        except (NXDOMAIN, NoNameservers, Timeout, NameError, NoAnswer):
            self.listed[self.dnslist]['ERROR'] = True


class RBLSearch(object):
    def __init__(self, cod, lookup_host):
        self.cod = cod
        self.lookup_host = lookup_host
        self._listed = None
        self.resolver = Resolver()
        self.resolver.timeout = 1.0
        self.resolver.lifetime = 5.0

    def search(self):
        if self._listed is not None:
            pass
        else:
            host = self.lookup_host.split(".")
            host = ".".join(list(reversed(host)))
            self._listed = {'SEARCH_HOST': self.lookup_host}
            threads = []
            for LIST in RBLS:
                self._listed[LIST] = {'LISTED': False}
                query = Lookup("%s.%s" % (host, LIST), LIST, self._listed, self.resolver)
                threads.append(query)
                query.start()
            for thread in threads:
                thread.join()
        return self._listed
    listed = property(search)

    def print_results(self):
        listed = self.listed

        for key in listed:
            if key == 'SEARCH_HOST':
                continue
            if not listed[key].get('ERROR'):
                if listed[key]['LISTED']:
                    self.cod.servicesLog("Results for %s: %s" % (key, listed[key]['LISTED']))
                    self.cod.servicesLog("+ Host information: %s" % \
                            (listed[key]['HOST']))
                if 'TEXT' in listed[key].keys():
                    self.cod.servicesLog(" + Additional information: %s" % \
                          (listed[key]['TEXT']))
            else:
                #print "*** Error contacting %s ***" % key
                pass

        self.cod.servicesLog("End of results")

if __name__ == "__main__":
    # Tests!
    try:
	if len(sys.argv) > 1:
		print "Looking up: %s (please wait)" % sys.argv[1]
	        searcher = RBLSearch(sys.argv[1])
        	searcher.print_results()
	else:
		print """Usage summary:

rblwatch <ip address to lookup> """
    except KeyboardInterrupt:
	pass
