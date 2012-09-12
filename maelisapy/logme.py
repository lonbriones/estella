""""""""""""""""""""""""""""""""" 
LogMe Controller
Author: Dionylon Briones
Date Created: January 14, 2009
Date Modified: January 14, 2009
"""""""""""""""""""""""""""""""""
from twisted.web import xmlrpc
from maelisapy.model import meta
from maelisapy.model import logme
from maelisapy import utils
from sqlalchemy import join
import re

session = meta.Session

class LogMeController:

	def getLogsByUserId(self, userid, limit, offset):
		offset = utils.offset(offset, limit)
		rows = session.query(logme.LogMe).filter('userid='+userid).limit(limit).offset(offset)
		count = session.query(logme.LogMe).filter('userid='+userid).count()
		ret = {}
		ret['count'] = count
		ret['data'] = utils.res('patronlog', rows)
		return ret

	def deleteLogByUserId(self, userid):
		rows = session.query(logme.LogMe).filter_by(userid=userid).all()
		try:
			session.delete(rows)
		except:
			raise
		return True

	def deleteLogById(self, id):
		row = session.query(logme.LogMe).get(id)
		if row:
			return session.delete(row)
		else:
			return False

	def addLog(self, data):
		log = logme.LogMe()
		for key in data:
			log.__dict__[key] = data[key]

		session.add(log)
		try:
			session.commit()
		except:
			session.rollback()
			raise

		return True
		

