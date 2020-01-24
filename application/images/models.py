from application import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    weight = db.Column(db.String(144), nullable=False)
    # method = db.Column(db.String(144), nullable=False)


    def __init__(self, weight):
        self.weight=weight
        # self.method=method