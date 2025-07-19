from datetime import datetime
from sqlalchemy import Column, DateTime

timestamp = Column(DateTime, default=datetime.utcnow)
