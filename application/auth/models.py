from application import db
from application.models import Base
from application.fish.models import Fish
from application.group.models import Group

from sqlalchemy.sql import text

# userGroup association
groups = db.Table('groups',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'),primary_key=True),
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'),primary_key=True)
)



class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(144), unique=True, nullable=False)
    password = db.Column(db.String(144), nullable=False)

    groups = db.relationship('Group', secondary=groups, backref=db.backref('accounts', lazy='joined'))
    fish = db.relationship("Fish",backref='account',lazy=True)

    def __init__(self, username,password):
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def roles(self):
        return ["ADMIN"]

    @staticmethod
    def find_users_with_no_posts(g_id):
        stmt = text("SELECT A.id, A.username" 
                     " FROM Account A CROSS JOIN "'"group"'" G CROSS JOIN groups gr"
                     " LEFT JOIN Fish ON Fish.group_id = :g_id"
                     " AND Fish.account_id = A.id"
                     " WHERE G.id = gr.group_id AND A.id = gr.account_id"
                     " AND G.id=:g_id AND (Fish.species IS null)").params(g_id=g_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"name":row[1]})

        return response


    @staticmethod
    def find_users_with_at_least_3_posts_in_group(g_id):

        stmt = text("SELECT A.id, A.username" 
                    " FROM Account A CROSS JOIN "'"group"'" G CROSS JOIN groups gr"
                    " LEFT JOIN Fish ON Fish.group_id = :g_id"
                    " AND Fish.account_id = A.id"
                    " WHERE G.id = gr.group_id AND A.id = gr.account_id"
                    " AND G.id=:g_id"
                    " GROUP BY A.id"
                    " HAVING COUNT(Fish.id) >= 3").params(g_id=g_id)
                        
        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"name":row[1]})

        return response

    @staticmethod
    def users_and_posts():

        stmt = text("SELECT Account.id, Account.username, COUNT(Fish.id) FROM Account"
                    " LEFT JOIN Fish ON Fish.account_id = Account.id"
                    " GROUP BY Account.id")
                        
        res = db.engine.execute(stmt)
        
        response = []

        for row in res:
           response.append({"id":row[0], "name":row[1], "count":row[2]})

        return response


