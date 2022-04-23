from models.user import UserModel
from flask_restful import reqparse, Resource
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type = str,
    required = True,
    help = "This field can't be left blank"
    )
    parser.add_argument('password',
    type = str,
    required = True,
    help = "This field can't be left blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'Msg':'User with name {} already exists'.format(data['username'])}
        user = UserModel(**data)
        user.save_to_db()
        return {'Msg':'User created successfully.'}