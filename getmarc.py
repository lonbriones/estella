""""""""""""""""""""""""""""""""" 
Export MARC 
Author: Dionylon Briones
Date Created: April 18, 2009
Date Modified: April 18, 2009
"""""""""""""""""""""""""""""""""
from maelisapy import init_maelisadb
from pymarc.field import Field
from pymarc.writer import MARCWriter
from pymarc.record import Record

#Change settings here
MARC_FILE = '/var/www/vufind/maedate/mae_%s.mrc'
DB = ''

engine = create_engine('firebird://SYSDBA:masterkey@localhost//opt/MAELISA2.GDB')
sm = orm.sessionmaker(autoflush=True, transactional=True, bind=engine)
meta.engine = engine
meta.Session = orm.scoped_session(sm)


def standardize_maemarc(fid, mae_marc, fname_suffix):
	marc_file = MARC_FILE % fname_suffix

	mae_marc = mae_marc.replace("\r", "")
	mae_marc = mae_marc.strip()
	mae_marc = mae_marc.rstrip("&")
	mae_marc = mae_marc.rstrip("%")
	
	parts = mae_marc.split('\n')

	header = parts[:2]
	tags_values =  parts[2:]
	ret = []

	writer = MARCWriter(file(marc_file, 'a+'))
	record = Record()
	control = parts[1:2][0][:-1]
	field = Field(tag = '001', data = fid)
	record.add_field(field)
	#field = Field(tag = '008', data = control) 
	#record.add_field(field)

	for dat in tags_values:
		dat = dat.strip('\n')
		tag = dat[0:3]
		values = []
		subfields = []
		for v in dat[6:-1].split('$'):
			subfield = v[:1]
			value = v[1:]
			if (tag == '260') and (subfield == 'c'):
				value = value.lstrip('c')
				value = value.rstrip(".")
				
			subfields.append(subfield)
			subfields.append(value)
			
		if tag == '245':
			indicator = ['1', '0']
		elif tag == '041':
			indicator = ['1', '0']
		else:
			indicator = ['', '']
		field = Field(tag, indicator, subfields)
		record.add_field(field)

		if tag:
			ret.append({tag:subfields})

	print "final output:"
	print record
	writer.write(record)
	writer.close()

"""
total = 472007.0
limit = 5000.0
"""
total = 1
limit = 1

from maelisapy.model import meta
from maelisapy.model import catalog
init_maelisadb()

marc = catalog.Marc
session = meta.Session
import math
step = int(math.ceil(total/limit))
for i in range(0, int(total), int(limit)):
	rows = session.query(marc).filter(marc.fid=='080628164443375').limit(limit).offset(i)
	print str(limit), ' ', str(i)
	j = 1
	for row in rows:
		print j
		standardize_maemarc(row.fid, row.marc, i)
		j += 1

"""
init_maelisadb()
from maelisapy import catalog
cat = catalog.CatalogController()

import math
step = int(math.ceil(total/limit))
for i in range(0, int(total), int(limit)):
	print str(limit), ' ', str(i)
	rows = cat.getCatalog('', int(limit), i);
	j = 1
	for row in rows['data']:
		print j
		standardize_maemarc(row['fid'], row['marc'], i)
		j += 1
"""
