from application import db
from application.models import Base

from sqlalchemy.sql import text

class Group(Base):

    name = db.Column(db.String(144), nullable=False)

    fish = db.relationship("Fish",backref='group',lazy=True)

    def __init__(self,name):
        self.name = name