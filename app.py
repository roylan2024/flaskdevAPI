from flask import Flask,request,jsonify
import uuid
from db import db
from flask_jwt_extended import JWTManager,create_refresh_token,get_jwt

#responsible API documentation
from flask_smorest import Api

#import the two blueprints
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

import os

from dotenv import load_dotenv

from blocklist import BLOCKLIST
from datetime import timedelta

from flask_migrate import Migrate

def create_app(db_url=None):
  
    app = Flask(__name__)
    
    #load all of the variables from .env
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['API_TITLE'] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"

    #DOCUMENTATION
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    #setup database we are going to use
    app.config["SQLALCHEMY_DATABASE_URI"]= db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    
    #connect flask alchemy to flask web app
    db.init_app(app)
    migrate = Migrate(app, db)
    
    #we need to create all the models we have designed
    #with app.app_context():  will be run by migrate already
    # db.create_all()
    
    #register blueprints
    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    
    #setup secret key for JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

    #create a jwt manager
    jwt = JWTManager(app)
    
    
    #setup for custom error messages
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "message": "The token has expired.", 
                    "error": "token_expired"
                }
            ),
            401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed.", 
                    "error": "invalid_token"
                }
            ),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request does not contain an access token.", 
                    "error": "authorization_required"
                }
            ),
            401
        )
        
    #Responsible for changes in JWT claims
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
      #user = UserModel.query.get(identity)
      #if user.is_admin == 1:
      if identity == 1:
        return {"is_admin": True}
      return {"is_admin": False}
    
    #checks everytime if the JTI of the JWT is in the blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        #True or False
        return jwt_payload["jti"] in BLOCKLIST
    
    
    return app 
        
if __name__ == '__main__':
     app = create_app()
     app.run(debug=True) 


# @app.get("/store")
# def get_stores():
#     return list(stores.values())

# @app.post("/store")
# def create_store():
#     store_data = request.get_json()  #data from postman json payload
#     store_id = uuid.uuid4().hex
    
#     if "name" in store_data:
   
#         for store in stores.values():
#             if store_data["name"] == store["name"]:
#                 return {"message":"Store alresdy exists."},400
            
#         new_store = {
#          "id": store_id,
#          "name": store_data["name"]   
#     }
      
    
#     stores.update({store_id:new_store})
#     return new_store,201
    
# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#     if store_id in stores:
#         return stores[store_id]
    
#     return {"message": "Store not found"},404    

# @app.post("/item")
# def add_item():
#     item_data = request.get_json()
    
#     if "name" in item_data and "price" in item_data and "store_id" in item_data:
#         for item in items.values():
#             if item["name"] == item_data["name"]:
#              return {"message": "Item name already exists"},400
            
    
#         if item_data["store_id"] in stores:
#             item_id = uuid.uuid4().hex
        
#             new_item = {
#               "id": item_id,
#               "name":item_data["name"],
#               "price":item_data["price"],
#               "store_id":item_data["store_id"]
#         }
#         items.update({item_id:new_item})
#         return new_item,201
        
#     return {"message": "Store not found"},404    

# @app.delete("/store/<string:store_id>")
# def detete_store(store_id):
#     if store_id in stores:
#         del stores[store_id]
#         return {"message":f"Store Deleted"}
#     else:
#         return {"message":"Store does not exist"},404

# @app.get("/item")
# def get_all_items():
#     return list(items.values())

# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     if item_id in items:
#         return items[item_id]
    
#     return {"message":"Item ID not found"},404

# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     if item_id in items:
#         del items[item_id]
#         return {"message":"Item deleted"}
#     else:
#         return {"message":"Item does not exist"},404

# @app.put("/item/<string:item_id>")
# def update_item(item_id):  
#     new_item_data = request.get_json()
    
#     if "name" in new_item_data or "price" in new_item_data:

#         if item_id in items:
     
#             item = items[item_id]
       
#             item |= new_item_data

        
#             return item
    
#     return {"nessage": "Item not found"},404
        
    
# @app.post("/items")   
# def multi_entry_items():
#     items_data = request.get_json() # is a List
# 
# #     new_items = []
#     for  item_data in items_data:
 #         if "name" in item_data and "price" in item_data and "store_id" in item_data:
#             for item in items.values():
 #                 if item["name"] == item_data["name"]:
#                 return {"message": f"Item name already exists: {item["name"]}"},400
                                            
                                    
 #             if item_data["store_id"] in stores:
#                 item_id = uuid.uuid4().hex
                                        
#                 new_item = {
 #                 "id": item_id,
#                 "name":item_data["name"],
 #                 "price":item_data["price"],
 #                 "store_id":item_data["store_id"]
  #             }
#             items.update({item_id:new_item})
 #             new_items.append(new_item)
                                        
#     return new_items,201
                                    