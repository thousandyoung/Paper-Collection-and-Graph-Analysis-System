from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Create a connection pool
engine = create_engine('sqlite:///spider.db', pool_size=10, max_overflow=20)

# Create a scoped session factory
Session = scoped_session(sessionmaker(bind=engine))