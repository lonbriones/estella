""""""""""""""""""""""""""""""""" 
Catalog Model
Author: Dionylon Briones
Date Created: November 16, 2008
Date Modified: December 27, 2008
"""""""""""""""""""""""""""""""""

import sqlalchemy as sa
from sqlalchemy import orm
from maelisapy.model import meta

t_marctags = sa.Table('tag', meta.metadata,
	sa.Column('tag', sa.types.String(), primary_key=True),
	sa.Column('suf', sa.types.String()),
	sa.Column('act', sa.types.String(1)),
	sa.Column('rpt', sa.types.String(1)),
	sa.Column('def', sa.types.String()),
)

t_jmarc = sa.Table('jmarc', meta.metadata,
	sa.Column('fid', sa.types.String(), primary_key=True),
	sa.Column('marc', sa.types.BLOB()),
	sa.Column('moudle', sa.types.String(1)),
	sa.Column('mtype', sa.types.String(1))
)

t_control = sa.Table('control', meta.metadata,
	sa.Column('accessno', sa.types.String(15), primary_key=True),
	sa.Column('fid', sa.types.String(), sa.ForeignKey('jmarc.fid')),
	sa.Column('barcode', sa.types.String(15)),
	sa.Column('callno', sa.types.String()),
	sa.Column('prfx', sa.types.String(10)),
	sa.Column('regdate', sa.types.Date),
	sa.Column('fldate', sa.types.Date),
	sa.Column('rent', sa.types.String()),
	sa.Column('location', sa.types.String(), sa.ForeignKey('location.code'))
)

t_location = sa.Table('location', meta.metadata,
	sa.Column('code', sa.types.String(15), primary_key=True),
	sa.Column('descrip', sa.types.String(200))
)

class Marc(object):
	def __repr__(self):
		return "Marc:\n%s\n%s\n%s\n%s" % (self.fid, self.marc, self.moudle, self.mtype)

class Holdings(object):
	def __repr__(self):
		return "Holdngs:'%s','%s','%s','%s','%s','%s','%s','%s','%s'" % (self.accessno, self.fid, self.barcode, self.callno, self.prfx, self.regdate, self.fldate, self.rent, self.location)

class Location(object):
	def __repr__(self):
		return "Location: '%s', '%s'" % (self.code, self.descrip)

orm.mapper(Marc, t_jmarc, properties={
	'holdings' : orm.relation(Holdings, 
		primaryjoin=t_jmarc.c.fid==t_control.c.fid,
		foreign_keys=[t_control.c.fid],
		cascade="all, delete, delete-orphan"
	)
})

class MarcTags(object):
	pass

orm.mapper(Location, t_location)
orm.mapper(MarcTags, t_marctags)
orm.mapper(Holdings, t_control)
