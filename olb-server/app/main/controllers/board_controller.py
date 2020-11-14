from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from ..models.board_dto import BoardDto
from ..services.board_service import search_boards, get_all_boards

api = BoardDto.namespace


@api.route("/<board_id>")
@api.param("board_id", "The specified board's id")
class GetBoard(Resource):

    @api.doc("Get the info of the board with the specified board id, token required", security="jwt")
    @api.marshal_with(BoardDto.board_profile_response)
    @jwt_required
    def get(self, board_id):
        stub = {
            "board_id": 1,
            "board_name": "Slap City",
            "is_public": True,
            "member_count": 10,
            "matches_count": 10,
            "top_members": [
                {
                    "name": "Joel",
                    "user_id": 1,
                    "rank_icon": 1,
                    "rank": 1,
                    "rating": 1400.1,
                    "wins": 10,
                    "losses": 5
                },
                {
                    "name": "Parker",
                    "user_id": 1,
                    "rank_icon": 1,
                    "rank": 2,
                    "rating": 1200.3,
                    "wins": 10,
                    "losses": 5
                }
            ]
        }
        return stub


@api.route("/<board_id>/activity")
@api.param("board_id", "The specified board's id")
class GetBoardActivity(Resource):

    @api.doc("Get the matches for the board with the specified board id, token required", security="jwt")
    @api.marshal_with(BoardDto.board_activity_response)
    @jwt_required
    def get(self, board_id):
        stub = {
            "matches": [
                {
                    "submitter_name": "Joel",
                    "receiver_name": "Parker",
                    "submitter_result": "Win",
                    "receiver_result": "Loss"
                },
                {
                    "submitter_name": "Jason",
                    "receiver_name": "Parker",
                    "submitter_result": "Win",
                    "receiver_result": "Loss"
                }
            ]
        }
        return stub


@api.route("/<board_id>/members")
@api.param("board_id", "The specified board's id")
class GetBoardMembers(Resource):

    @api.doc("Get the members the board with the specified board id, token required", security="jwt")
    @api.marshal_with(BoardDto.board_members_response)
    @jwt_required
    def get(self, board_id):
        stub = {
            "members": [
                {
                    "name": "Joel",
                    "user_id": 1,
                    "rank_icon": 1,
                    "rank": 1,
                    "rating": 1400.1,
                    "wins": 10,
                    "losses": 5
                },
                {
                    "name": "Parker",
                    "user_id": 1,
                    "rank_icon": 1,
                    "rank": 2,
                    "rating": 1200.3,
                    "wins": 10,
                    "losses": 5
                }
            ]
        }
        return stub


@api.route("/create")
class CreateBoard(Resource):

    @api.doc("Create new board", security="jwt")
    @api.expect(BoardDto.create_board, validate=True)
    @api.marshal_with(BoardDto.create_board_response)
    @jwt_required
    def post(self):
        user_data = request.json
        stub = {
            "success": True,
            "message": "Successfully created",
            "board_id": 3
        }
        return stub


@api.route("/edit")
class EditBoard(Resource):

    @api.doc("Edit existing board", security="jwt")
    @api.expect(BoardDto.edit_board, validate=True)
    @api.marshal_with(BoardDto.edit_board_response)
    @jwt_required
    def post(self):
        user_data = request.json
        stub = {
            "success": True,
            "message": "Successfully edited board"
        }
        return stub


@api.route("/invite")
class InviteUserToBoard(Resource):

    @api.doc("Invite a user to a board", security="jwt")
    @api.expect(BoardDto.invite_to_board, validate=True)
    @api.marshal_with(BoardDto.invite_to_board_response)
    @jwt_required
    def post(self):
        user_data = request.json
        stub = {
            "success": True,
            "message": "Invite successfully created",
        }
        return stub


@api.route("/join")
class JoinBoard(Resource):

    @api.doc("Join a board", security="jwt")
    @api.expect(BoardDto.join_board, validate=True)
    @api.marshal_with(BoardDto.join_board_response)
    @jwt_required
    def post(self):
        user_data = request.json
        stub = {
            "success": True,
            "message": "Successfully joined board",
        }
        return stub


@api.route("/remove")
class RemoveUserFromBoard(Resource):

    @api.doc("Leave a board/remove a user from a board", security="jwt")
    @api.expect(BoardDto.remove_from_board, validate=True)
    @api.marshal_with(BoardDto.remove_from_board_response)
    @jwt_required
    def post(self):
        user_data = request.json
        stub = {
            "success": True,
            "message": "Successfully left board",
        }
        return stub


@api.route("/search")
class GetAllBoards(Resource):

    @api.doc("Get all boards, token required", security="jwt")
    @api.marshal_with(BoardDto.board_search_response)
    @jwt_required
    def get(self):
        return get_all_boards()


@api.route("/search/<board_name>")
@api.param("board_name", "The board name being searched")
class SearchBoards(Resource):

    @api.doc("Search for boards containing <board_name> string, token required", security="jwt")
    @api.marshal_with(BoardDto.board_search_response)
    @jwt_required
    def get(self, board_name):
        return search_boards(board_name)
