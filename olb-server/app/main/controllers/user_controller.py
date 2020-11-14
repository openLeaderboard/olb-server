from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.user_dto import UserDto
from ..services.user_service import create_user, search_users, get_all_users,\
                                    get_normal_user_boards, get_admin_user_boards, get_favourite_user_boards,\
                                    get_user_profile, get_user_activity

api = UserDto.namespace


@api.route("/<user_id>")
@api.param("user_id", "The specified user's id")
class GetUserProfile(Resource):

    @api.doc("Get the profile info of the user with the specified user id, token required", security="jwt")
    @api.marshal_with(UserDto.user_profile_response)
    @jwt_required
    def get(self, user_id):
        return get_user_profile(user_id)


@api.route("/<user_id>/activity")
@api.param("user_id", "The specified user's id")
class GetUserActivity(Resource):

    @api.doc("Get the activity of the user with the specified user id, token required", security="jwt")
    @api.marshal_with(UserDto.user_activity_response)
    @jwt_required
    def get(self, user_id):
        response = {
            "matches": get_user_activity(user_id)
        }
        return response


@api.route("/<user_id>/boards")
@api.param("user_id", "The specified user's id")
class GetUserBoards(Resource):

    @api.doc("Get the boards of the user with the specified user id, token required", security="jwt")
    @api.marshal_with(UserDto.user_boards_response)
    @jwt_required
    def get(self, user_id):
        response = {
            "boards": get_normal_user_boards(user_id)
        }
        return response


@api.route("/activity")
class GetMyActivity(Resource):

    @api.doc("Get the activity of the logged in user, token required", security="jwt")
    @api.marshal_with(UserDto.user_activity_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "matches": get_user_activity(user_id)
        }
        return response


@api.route("/boards")
class GetMyBoards(Resource):

    @api.doc("Get the boards of the logged in user, token required", security="jwt")
    @api.marshal_with(UserDto.user_boards_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "boards": get_normal_user_boards(user_id)
        }
        return response


@api.route("/boards/mine")
class GetMyCreatedBoards(Resource):

    @api.doc("Get the boards created by the logged in user, token required", security="jwt")
    @api.marshal_with(UserDto.user_boards_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "boards": get_admin_user_boards(user_id)
        }
        return response


@api.route("/boards/favourites")
class GetMyFavouriteBoards(Resource):

    @api.doc("Get the favourite boards of the logged in user (should be a max of 5), token required", security="jwt")
    @api.marshal_with(UserDto.user_boards_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "boards": get_favourite_user_boards(user_id)
        }
        return response


@api.route("/boards/notfavourites")
class GetMyNotFavouriteBoards(Resource):

    @api.doc("Get the boards that are not favourites of the logged in user (for selecting new favourites), token required", security="jwt")
    @api.marshal_with(UserDto.user_boards_response)
    @jwt_required
    def get(self):
        stub = {
            "boards": [
                {
                    "board_name": "Slap City",
                    "board_id": 1,
                    "rank_icon": 1,
                    "rank": 1,
                    "users_count": 56,
                    "rating": 1400.1,
                    "wins": 10,
                    "losses": 5
                },
                {
                    "board_name": "Joel's Board",
                    "board_id": 2,
                    "rank_icon": 1,
                    "rank": 2,
                    "users_count": 56,
                    "rating": 1200.4,
                    "wins": 10,
                    "losses": 5
                },
            ]
        }
        return stub


@api.route("/favourite")
class AddRemoveFavouriteBoard(Resource):

    @api.doc("Add or remove a board to/from favourites", security="jwt")
    @api.expect(UserDto.favourite_board, validate=True)
    @api.marshal_with(UserDto.favourite_board_response)
    @jwt_required
    def post(self):
        user_data = request.json
        stub = {
            "success": True,
            "message": "Successfully added board to favourites"
        }
        return stub


@api.route("/profile")
class GetMyProfile(Resource):

    @api.doc("Get the profile info of the logged in user, token required", security="jwt")
    @api.marshal_with(UserDto.user_profile_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return get_user_profile(user_id)


@api.route("/register")
class RegisterUser(Resource):

    @api.doc("Create a new user")
    @api.expect(UserDto.register_user, validate=True)
    @api.marshal_with(UserDto.register_user_response)
    def post(self):
        user_data = request.json
        return create_user(user_data=user_data)


@api.route("/search")
class GetAllUsers(Resource):

    @api.doc("Get all users, token required", security="jwt")
    @api.marshal_with(UserDto.user_search_response)
    @jwt_required
    def get(self):
        response = {
            "search_result": get_all_users()
        }
        return response


@api.route("/search/<username>")
@api.param("username", "The username being searched")
class SearchUsers(Resource):

    @api.doc("Search for users containing <username> string, token required", security="jwt")
    @api.marshal_with(UserDto.user_search_response)
    @jwt_required
    def get(self, username):
        response = {
            "search_result": search_users(username)
        }
        return response
