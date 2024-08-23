from db import db

#design model for store
class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False,unique=True)
    
    #define relationship 
    # one to many - could have more than one item 
    items = db.relationship("ItemModel",back_populates="store",lazy="dynamic",cascade="all, delete")
    #relationship tag  and store one to many
    tags = db.relationship("TagModel",back_populates="store",lazy="dynamic",cascade="all, delete")
    