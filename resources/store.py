from models.store import StoreModel
from flask_restful import Resource

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'Msg':'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Msg':'Store named {} already exists'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'Msg':'Error occured'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'Msg':'Store deleted'}
        return {'Msg':'Store not found'}, 404

    
class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x:x.json(), StoreModel.query.all()))}