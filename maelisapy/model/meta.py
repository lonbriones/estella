""""""""""""""""""""""""""""""""" 
Meta
Author: Dionylon Briones
Date Created: November 16, 2008
Date Modified: December 27, 2008
"""""""""""""""""""""""""""""""""

"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Session', 'metadata']

# SQLAlchemy database engine.  Updated by model.init_model()
engine = None

# SQLAlchemy session manager.  Updated by model.init_model()
Session = None

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()
