from models.item import ItemModel
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field can't be left balnk"
    )
    parser.add_argument('store_id',
    type = int,
    required = True,
    help = "This field can't be left balnk"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'Msg':'Item not found.'}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Msg':'Item with name {} already exists'.format(name)}
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'Msg':'Error ocurred'}, 400
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'Msg':'Item deleted'}
        return {'Msg':'Item not found'}

    def put(self, name):
        data =Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()
        

class ItemList(Resource):
    def get(self):
        return {'items':list(map(lambda x:x.json(), ItemModel.query.all()))}