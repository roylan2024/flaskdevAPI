
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort

from schemas import ItemSchema,ItemUpdateSchema

from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import jwt_required

blp = Blueprint("items",__name__,description="Operations in items")

# blp.arguments = papasok na data
#blp.response = palabas na data

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required()
    #validation for the response
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        # if item_id in items:
        #  return items[item_id]
        
        # #return {"message":"Item ID not found"},404
        # abort(404,message="Item not found")
    @jwt_required(fresh=True)   
    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        #Delete an item
        db.session.delete(item)
        db.session.commit()
        
        return {"message": "Item Deleted"}
        # if item_id in items:
        #     del items[item_id]
        #     return {"message":"Item deleted"}
        # else:
        #     abort(404,message="Item does not exists.")
           
            #return {"message":"Item does not exist"},404  
    @jwt_required(fresh=True)
    #Data validation of update       
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,new_item_data,item_id):
        item = ItemModel.query.get(item_id)
        
        if item:
            item.name = new_item_data["name"]
            item.price = new_item_data["price"]    
        else:
            #create new item
            item = ItemModel(**new_item_data)
            
        db.session.add(item)
        db.session.commit()   
         
        return item
       # new_item_data = request.get_json()
    
        #if "name" in new_item_data or "price" in new_item_data:

        # if item_id in items:
        #     item = items[item_id]
        #     item |= new_item_data

        #     return item
        # abort(404,message="Item not found")
        #return {"nessage": "Item not found"},404

@blp.route("/item")   
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True)) # list many items
    def get(self):
        return ItemModel.query.all()
        # return list(items.values())  
    
    #Data Validation JSON go to Blp.Arg then Method
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def post(self,item_data):
        new_item = ItemModel(**item_data)
        
        try:
            #add new item to the session
            db.session.add(new_item)
            #save changes
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="an error occured while creating an item")
        return new_item,201  
        #item_data = request.get_json()
    
        #if "name" in item_data and "price" in item_data and "store_id" in item_data:
        # for item in items.values():
        #   if (
        #       item["name"] == item_data["name"] 
        #       and item_data["store_id"] == item["store_id"]
        #      ):       
        #       abort(400,message="Item already exists")
        #         #return {"message": "Item name already exists"},400
                
        
        #   if item_data["store_id"] in stores:
        #          item_id = uuid.uuid4().hex
            
        #          new_item = {
        #         "id": item_id,
        #         "name":item_data["name"],
        #         "price":item_data["price"],
        #         "store_id":item_data["store_id"]
        #     }
        # items.update({item_id:new_item})
        # return new_item,201
        
        # abort(404,message="Item not found")    
        # #return {"message": "item not found"},404            