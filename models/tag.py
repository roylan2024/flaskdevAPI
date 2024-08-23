from db import db

class TagModel(db.Model):
    __tablename__ ="tags"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=False,nullable=False)
    
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"),nullable=False)
    
    #define relationship betwoeen tag and store
    store = db.relationship("StoreModel",back_populates ="tags")
    
    #define many-many relationship with items
    items = db.relationship("ItemModel",back_populates="tags",secondary="item_tags")