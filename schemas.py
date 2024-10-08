from marshmallow import Schema,fields


class PlainItemSchema(Schema):
    #define fields
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    #store_id = fields.Str(required=True)
       
    
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)   
    name = fields.Str(required=True)
    
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)   
    name = fields.Str(required=True)
    
class ItemUpdateSchema(Schema):
    #optional 
    name = fields.Str()   
    price = fields.Float()
    #idempotency
    store_id = fields.Int()
    
class ItemSchema(PlainItemSchema):
     store_id = fields.Int(required=True) 
     store = fields.Nested(PlainStoreSchema(),dump_only=True)
     tags = fields.List(fields.Nested(PlainTagSchema),dump_only=True)
     
class TagSchema(PlainTagSchema):
     store_id = fields.Int(load_only=True) 
     store = fields.Nested(PlainStoreSchema(),dump_only=True)    
     
     items = fields.List(fields.Nested(PlainTagSchema),dump_only=True)
     
class StoreSchema(PlainStoreSchema):
      items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)  
    
#used for unlinking the tag      
class TagAndItemsSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(TagSchema()) 
    
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)
    #password = fields.Str(required=True)    
    
#adding comments   
    # import secrets
    
    # print(secrets.SystemRandom().getrandbits(128))
    
         