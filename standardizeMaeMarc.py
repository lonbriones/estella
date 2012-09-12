"""
Standardize Maelisa Marc
------------------------------------------------
This script will do the following procedures:
1. Get the Maelisa marc from the database
2. Convert them to Marc21
3. Save them to a file.

Author: Dionylon Briones

Todo:
  Include the indicators (this may introduce a bug)
"""

from pymarc.field import Field
from pymarc.writer import MARCWriter
from pymarc.record import Record

mae_marc = """
000nam a%
008460911s1936    us            000   eng  %
041  $aeng%
090  $aPN6331$bE2 1936%
100  $aEdwards, Tryon%
245  $aThe new dictionary of thoughts : a cyclopedia of quotations from the best authors of the world, both ancient and modern /$cEdwards, Tryon%
260  $aNew York :$bStandard Book$c1936 ,$c1936.%
300  $a734%
650  $aQuotations, English%
700  $frev.% enl.$sCatrevas$gC. N.%
959  $a09/11/1946%
993  $aR%
994  $amonograph&
"""

marc_file = '/var/www/vufind/maemarc.mrc'
fid = 'lonl123123'
def standardize_maemarc(fid, mae_marc):
	print mae_marc
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
	field = Field(tag = '008', data = control) 
	record.add_field(field)

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
			
		field = Field(tag, ['', ''], subfields)
		record.add_field(field)

		if tag:
			ret.append({tag:subfields})

	print "final output:"
	print record
	writer.write(record)
	writer.close()
	#print ret
standardize_maemarc(fid, mae_marc)
