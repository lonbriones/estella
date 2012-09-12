print "MaelisaPy Server"
print "Written by: Dionylon Briones"
print "Maelisa init..."

from maelisapy import init_maelisadb

init_maelisadb()

from maelisapy.catalog import Catalog
from twisted.internet import reactor
from twisted.web import server


catalog = Catalog()

reactor.listenTCP(8000, server.Site(catalog))
print "Running..."
print "\nPress CTRL-C to stop"
reactor.run()
