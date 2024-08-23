

from flask import request

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import jwt_required


blp = Blueprint("store",__name__,description= "Operation on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        #  if store_id in stores:
        #   return stores[store_id]
      
        #  abort(404,message="Store not found")
        # # return {"message": "Store not found"},404   
    
    #required a frsh token
    @jwt_required(fresh=True)
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        
        db.session.delete(store)
        db.session.commit()
        
        return {"message": "Store Deleted"}
        #  if store_id in stores:
        #     del stores[store_id]
        #     return {"message":f"Store Deleted"}
        #  else:
             
        #     abort(400,message="Store does not exist.") 
            #return {"message":"Store does not exist"},404

@blp.route("/store")
class StoreList(MethodView): 
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
        # return list(stores.values())
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,new_store_data):
        store = StoreModel(**new_store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="an error has occured while creating a store") 
               
        return store,201
        # store_data = request.get_json()  #data from postman json payload
        # store_id = uuid.uuid4().hex
    
        # #if "name" in store_data:
    
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400,message="Store already exists.")
        #         #return {"message":"Store alresdy exists."},400
            
        # new_store = {
        # "id": store_id,
        # "name": store_data["name"]   
        # }
    
        
        # stores.update(
        #     {store_id:new_store}
        # )
        # return new_store,201
        
        
        