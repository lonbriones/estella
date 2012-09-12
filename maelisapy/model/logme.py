""""""""""""""""""""""""""""""""" 
LogMe Model
Author: Dionylon Briones
Date Created: January 14, 2009
Date Modified: January 14, 2009
"""""""""""""""""""""""""""""""""

import sqlalchemy as sa
from sqlalchemy import orm
from maelisapy.model import meta

t_patronlog = sa.Table('patronlog', meta.metadata,
	sa.Column('plogno', sa.types.Integer(), primary_key=True),
	sa.Column('userid', sa.types.String()),
	sa.Column('timein', sa.DateTime()),
	sa.Column('timeout', sa.DateTime()),
	sa.Column('terminal', sa.String())
)

class LogMe(object):
	def __repr__(self):
		return "PatronLog: %d %d %s %s %s" % (self.plogno, self.userid, self.timein, self.timeout, self.terminal)

orm.mapper(LogMe, t_patronlog)
