from application import db


class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    species = db.Column(db.String(144), nullable=False)
    weight = db.Column(db.Numeric(precision=4, asdecimal=False, decimal_return_scale=None))
    # method = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)

    def __init__(self, species):
        self.species = species
        self.weight = 0
        # self.method=method
