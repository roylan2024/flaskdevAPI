from flask import request

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import TagSchema,TagAndItemsSchema
from models import TagModel,StoreModel,ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

#STORE AND TAGD ENDPOINTS
# /store/<id>/tag -POST crete tag inside a store
# /store/<id>/tag - GET get all tags inside a store

# TAG ENDPOINTS
#/tag/<id>   GET get a tag by ID
#/tag/<id>   DELETE deelte a tag by ID

# ITEM AND TAGS ENDPOINTS
#/item/<item_id>/tag/<tag-id> POST link tag to an item
#/item/<item_id>/tag/<tag_id> DELETE unlink tag to an item


blp = Blueprint("tags",__name__,description="Operation on tags")

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    def delete(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        
        #check if has items linked
        if tag.items:
            abort(400,message="Could not delete tag,make tag is not link to any item")
        
        db.session.delete(tag)
        db.session.commit()
        
        return {"message": "Tag deleted"},202
    
@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self,new_tag_data,store_id):
        #check if the new tag is already in the store
        if TagModel.query.filter(
            TagModel.store_id == store_id,
            TagModel.name == new_tag_data["name"]   
        ).first():
            abort(400,message="A tag with that name already exists in the store")
        tag = TagModel(**new_tag_data,store_id=store_id) 
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="an error occured while creting a tag") 
        return tag   
    
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")    
class LinkTagsToItem(MethodView):
    #Link tag to an item
    
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
    #before linking make sure that the item and the tag is inside the same store
        if item.store_id != tag.store_id:
          abort(400,message="Make sure that the item and the tag belongs to the same store before linking")  
           
        item.tags.append(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occured while linking the tag")  
            
        return tag   
       
    @blp.response(200,TagAndItemsSchema)
    def delete(self,item_id,tag_id):
          item = ItemModel.query.get_or_404(item_id)
          tag = TagModel.query.get_or_404(tag_id)  
          
          #updated the list of tags
          item.tags.remove(tag)
          
          try:
              
              db.session.add(item)
              db.session.commit()
          except SQLAlchemyError:
              abort(500,message="An error occured while unlinking the tag") 
               
          return {"message": "Item removed from the tag","item":item,"tag":tag}      
             
            
             