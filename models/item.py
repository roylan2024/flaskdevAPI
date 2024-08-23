from db import db

class ItemModel(db.Model):
    
    __tablename__="items"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    price = db.Column(db.Float,unique=False,nullable=False)
    #description=db.Column(db.String(200),nullable=True)
    
    #define this column as foreign key
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False,nullable=False)
    
    #define rrelationship itemModel and StoreModel  tables
    store = db.relationship("StoreModel",back_populates="items")
    #connect the itemmodel to have tags column
    tags = db.relationship("TagModel",back_populates="items",secondary="item_tags")