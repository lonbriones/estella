from maelisapy import init_maelisadb
from maelisapy.model import meta
from maelisapy.model import catalog

init_maelisadb()
holdings_res = meta.Session.query(catalog.Holdings).filter_by(fid='080221151513375').all()

for row in holdings:
    print row.accessno

