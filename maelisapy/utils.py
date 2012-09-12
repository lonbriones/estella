from maelisapy.model import catalog

__all__ = ['assoc', 'res']

def assoc(table_name, row):
	ret = {}
	for col in catalog.meta.metadata.tables[table_name].columns:
		val = row.__dict__[col.name]
		if val == None:
			val = ''
		ret[col.name] = val
	return ret

def res(table_name, res):
	ret = []
	for row in res:
		ret.append(assoc(table_name, row))
	return ret

def authenticate(token):
	return True

def offset(offset, limit):
	if offset <= 1: 
		offset = 0
	else:
		offset = (offset * limit) - 1

	return offset
