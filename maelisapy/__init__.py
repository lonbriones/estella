from sqlalchemy import create_engine
from maelisapy.model import init_model

def init_maelisadb():
	engine = create_engine('firebird://SYSDBA:masterkey@localhost//opt/MAELISA2.GDB')
	init_model(engine)

