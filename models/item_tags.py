from db import db

#Conjunction table
class ItemTags(db.Model):
    __tablename__ = "item_tags"
    
    id = db.Column(db.Integer,primary_key=True)
    
    #define 2 foreign keys
    item_id = db.Column(db.Integer,db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id"))
    
   
    