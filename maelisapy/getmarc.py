""""""""""""""""""""""""""""""""" 
Export MARC 
Author: Dionylon Briones
Date Created: April 18, 2009
Date Modified: April 18, 2009
"""""""""""""""""""""""""""""""""
from twisted.web import xmlrpc
from maelisapy.model import meta
from maelisapy.model import catalog
from maelisapy import utils
from sqlalchemy import join
import re

marc = catalog.Marc
holdings = catalog.Holdings
session = meta.Session

filter = ''
limit = 1
offset = 1

rows = session.query(marc).join(holdings).filter(filter).limit(limit).offset(offset)
print rows
