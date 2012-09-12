""""""""""""""""""""""""""""""""" 
Catalog Module
Author: Dionylon Briones
Date Created: November 16, 2008
Date Modified: December 28, 2008
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

class CatalogController:

	def getCatalog(self, filter, limit, offset):

		offset = utils.offset(offset, limit)
		has_holdings_table = False

		for col in catalog.meta.metadata.tables['control'].columns:
			if re.match('('+col.name+')', filter):
				has_holdings_table = True
				break;

		if not filter:
			rows = session.query(marc).limit(limit).offset(offset)
			count = session.query(marc).count()
		elif has_holdings_table:
			rows = session.query(marc).join(holdings).filter(filter).limit(limit).offset(offset)
			count = session.query(marc).join(holdings).filter(filter).count()
		else:
			rows = session.query(marc).filter(filter).limit(limit).offset(offset)
			count = session.query(marc).filter(filter).count()

		ret = {}
		ret['count'] = count
		ret['data'] = self.all(rows)
		return ret
		
	def getCatalogByBarcode(self, barcode):
		return self.one(session.query(marc).join(holdings).filter_by(barcode=barcode).one())

	def assignBarcode(self, accessno, barcode):
		row = session.query(holdings).filter_by(accessno=accessno).one()
		row.barcode = barcode
		try:
			session.commit()
			ret = True
		except:
			session.rollback()
			ret = False
			raise

		return ret
		
	def getCatalogById(self, id):
		return self.one(session.query(marc).get(id))
	
	def getCatalogByAccessNo(self, accessno):
		return self.one(session.query(marc).select_from(catalog.t_jmarc.join(catalog.t_control)).filter(holdings.accessno==accessno).one())

	def getCatalogByLocation(self, location, limit, offset):
		return self.getCatalog("location='"+location+"'", limit, offset)

	def getCatalogByMaterialType(self, type, limit, offset):
		return self.getCatalog("mtype='"+type+"'", limit, offset)

	def save(self, data):

		# check marc if exists
		id = data['fid']
		marc = session.query(catalog.Marc).get(id)

		if marc: 
			marc_exists = True
		else: 
			marc_exists = False
			marc = catalog.Marc()

		# map the data, but skip holdings info
		for key in data:	
			if key != 'holdings':
				marc.__dict__[key] = data[key]

		
		# before we map the holdings info, delete them first from the database
		holds = session.query(catalog.Holdings).filter_by(fid=id)
		for row in holds:
			session.delete(row)
		
		# here's the saving of the holdings info
		for row in data['holdings']:	
			holds = catalog.Holdings()

			for key in row: 
				holds.__dict__[key] = row[key]

			marc.holdings.append(holds)
		
		try:
			if not marc_exists: 
				session.add(marc)
			session.commit()
		except:
			session.rollback()
			raise

		return True


	def deleteAccessNo(self, accessno):

		try:
			row = session.query(catalog.Holdings).filter_by(accessno=accessno).one()
			session.delete(row)
			session.commit()
		except:
			session.rollback()
			return False

		return True
		

	def deleteCatalog(self, id):
		#delete all accession numbers
		marc = session.query(catalog.Marc).get(id)
		ret = True
		try:
			session.delete(marc)
			session.commit()
		except:
			session.rollback()
			ret = False

		return ret

	def all(self, rows):
		ret = []
		for row in rows:
			ret.append(self.one(row))
		return ret

	def one(self, row):
		ret = utils.assoc('jmarc', row)
		ret['holdings'] = utils.res('control', row.holdings)
		return ret

	def renameLocation(self, old_code, new_code, new_description):
		location = session.query(catalog.Location).get(old_code)

		if not location: return False

		rows = session.query(catalog.Holdings).filter_by(location=old_code).all()
		for row in rows:
			row.location = new_code
		
		session.delete(location)

		location = catalog.Location()
		location.code = new_code
		location.descrip = new_description

		try:
			session.commit()
		except:
			session.rollback()
			raise

		return True
	

	def deleteLocation(self, code):
		location = session.query(catalog.Location).get(code)
		try:
			session.delete(delete)
			session.commit()
		except:
			session.rollback()

		return True

	def addLocation(self, code, description):
		location = session.query(catalog.Location).get(code)

		if location: return False	

		location = catalog.Location()
		location.code = code
		location.description = description

		try:
			session.add(location)
			session.commit()
		except:
			session.rollback()
			raise

		return True

	def getMarcTags(self):
		rows = session.query(catalog.MarcTags).all()
		return utils.res('tag', rows)


	def addMarcTag(self, tag, suffix, visible, repeatable, description):
		marctag = session.query(catalog.MarcTags).get(tag)
			
		if not marctag:
			marctag = catalog.MarcTags()
			marctag.tag = tag
			marctag.suffix = suffix
			marctag.visible = visible
			marctag.repeatable = repeatable
			marctag.description = description
			session.add(marctag)
		else:
			marctag.tag = tag
			marctag.suffix = suffix
			marctag.visible = visible
			marctag.repeatable = repeatable
			marctag.description = description

		try:
			session.commit()
		except:
			session.rollback()
			raise

		return True

		
	def deleteMarcTag(self, tag):
		marctag = session.query(catalog.MarcTags).get(tag)
		session.delete(marctag)
		try:
			session.commit()
		except:
			session.rollback()
			raise

		return True



catalog_controller = CatalogController()

class Catalog(xmlrpc.XMLRPC):
        
	def xmlrpc_add(self, a, b):
		return a + b

	##################################################
	# Manage marc/holdings
	##################################################
	def xmlrpc_getCatalog(self, token, filter, limit, offset):
		if not utils.authenticate(token): return false
		return catalog_controller.getCatalog(filter, limit, offset)

	def xmlrpc_saveCatalog(self, token, data):
		if not utils.authenticate(token): return false
		return catalog_controller.save(data)
	
	def xmlrpc_deleteCatalog(self, token, fid):
		if not utils.authenticate(token): return false
		return catalog_controller.delete(fid)

	def xmlrpc_deleteAccessNo(self, token, accessno):
		if not utils.authenticate(token): return false
		return catalog_controller.deleteAccessNo(accessno)

	def xmlrpc_getCatalogById(self, token, id):
		if not utils.authenticate(token): return false
		return catalog_controller.getCatalogById(id)

	def xmlrpc_getCatalogByAccessNo(self, token, accessno):
		if not utils.authenticate(token): return false
		return catalog_controller.getCatalogByAccessNo(accessno)


	##################################################
	# Manage barcode bindings
	##################################################
	def xmlrpc_getCatalogByBarcode(self, token, barcode):
		if not utils.authenticate(token): return false
		return catalog_controller.getCatalogByBarcode(barcode)

	def xmlrpc_assignBarcode(self, token, accessno, barcode):
		if not utils.authenticate(token): return false
		return catalog_controller.assignBarcode(accessno, barcode)

	def xmlrcp_deleteBarcode(self, token, accessno):
		if not utils.authenticate(token): return false
		return catalog_controller.assignBarcode(accessno, '')


	##################################################
	# Manage locations
	##################################################
	def xmlrpc_getCatalogByLocation(self, token, location):
		if not utils.authenticate(token): return false
		return catalog_controller.getCatalogByLocation(location)

	def xmlrpc_addLocation(self, token, code, description):
		if not utils.authenticate(token): return false
		return catalog_controller.addLocation(code, description)

	def xmlrpc_renameLocation(self, token, old_code, new_code, new_description):
		if not utils.authenticate(token): return false
		return catalog_controller.renameLocation(old_code, new_code, new_description)

	def xmlrpc_deleteLocation(self, token, code):
		if not utils.authenticate(token): return false
		return catalog_controller.deleteLocation(code)

	##################################################
	# Manage marc tags
	##################################################
	def xmlrpc_getMarcTags(self, token):
		if not utils.authenticate(token): return false
		return catalog_controller.getMarcTags()

	def xmlrpc_addMarcTag(self, token, tag, suffix, visible, repeatable, description):
		return catalog_controller.addMarcTag(tag, suffix, visible, repeatable, description)
