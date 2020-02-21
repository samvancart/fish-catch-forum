from application import db
from application.models import Base


class Fish(Base):

    species = db.Column(db.String(144), nullable=False)
    weight = db.Column(db.Numeric(precision=4, asdecimal=False, decimal_return_scale=None))
    image_file = db.Column(db.String(20))
    image_blob = db.Column(db.LargeBinary)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'),
                            nullable=False)

    def __init__(self, species):
        self.species = species
        self.weight = 0
        image_file = ""