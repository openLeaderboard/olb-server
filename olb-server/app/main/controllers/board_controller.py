from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.board_dto import BoardDto
from ..services.board_service import (
    search_boards,
    get_all_boards,
    get_board_activity,
    get_normal_board_users,
    get_board_profile,
    create_board,
    edit_board,
    invite_to_board,
    join_board,
    leave_board,
    remove_from_board,
)

api = BoardDto.namespace


@api.route("/<board_id>")
@api.param("board_id", "The specified board's id")
class GetBoard(Resource):
    @api.doc("Get the info of the board with the specified board id, token required", security="jwt")
    @api.marshal_with(BoardDto.board_profile_response)
    @jwt_required
    def get(self, board_id):
        user_id = get_jwt_identity()
        return get_board_profile(board_id, user_id)


@api.route("/<board_id>/activity")
@api.param("board_id", "The specified board's id")
class GetBoardActivity(Resource):
    @api.doc("Get the matches for the board with the specified board id, token required", security="jwt")
    @api.marshal_with(BoardDto.board_activity_response)
    @jwt_required
    def get(self, board_id):
        response = {
            "matches": get_board_activity(board_id),
        }
        return response


@api.route("/<board_id>/members")
@api.param("board_id", "The specified board's id")
class GetBoardMembers(Resource):
    @api.doc("Get the members the board with the specified board id, token required", security="jwt")
    @api.marshal_with(BoardDto.board_members_response)
    @jwt_required
    def get(self, board_id):
        response = {
            "members": get_normal_board_users(board_id),
        }
        return response


@api.route("/create")
class CreateBoard(Resource):
    @api.doc("Create new board", security="jwt")
    @api.expect(BoardDto.create_board, validate=True)
    @api.marshal_with(BoardDto.create_board_response)
    @jwt_required
    def post(self):
        create_board_data = request.json
        return create_board(create_board_data)


@api.route("/edit")
class EditBoard(Resource):
    @api.doc("Edit existing board", security="jwt")
    @api.expect(BoardDto.edit_board, validate=True)
    @api.marshal_with(BoardDto.edit_board_response)
    @jwt_required
    def post(self):
        edit_board_data = request.json
        return edit_board(edit_board_data)


@api.route("/invite")
class InviteUserToBoard(Resource):
    @api.doc("Invite a user to a board", security="jwt")
    @api.expect(BoardDto.invite_to_board, validate=True)
    @api.marshal_with(BoardDto.invite_to_board_response)
    @jwt_required
    def post(self):
        invite_data = request.json
        return invite_to_board(invite_data)


@api.route("/join")
class JoinBoard(Resource):
    @api.doc("Join a board", security="jwt")
    @api.expect(BoardDto.join_board, validate=True)
    @api.marshal_with(BoardDto.join_board_response)
    @jwt_required
    def post(self):
        join_data = request.json
        return join_board(join_data)


@api.route("/remove")
class RemoveUserFromBoard(Resource):
    @api.doc("Leave a board/remove a user from a board", security="jwt")
    @api.expect(BoardDto.remove_from_board, validate=True)
    @api.marshal_with(BoardDto.remove_from_board_response)
    @jwt_required
    def post(self):
        remove_data = request.json
        if remove_data["remove"]:
            return remove_from_board(remove_data)
        else:
            return leave_board(remove_data)


@api.route("/search")
class GetAllBoards(Resource):
    @api.doc("Get all boards, token required", security="jwt")
    @api.marshal_with(BoardDto.board_search_response)
    @jwt_required
    def get(self):
        response = {
            "search_result": get_all_boards(),
        }
        return response


@api.route("/search/<board_name>")
@api.param("board_name", "The board name being searched")
class SearchBoards(Resource):
    @api.doc("Search for boards containing <board_name> string, token required", security="jwt")
    @api.marshal_with(BoardDto.board_search_response)
    @jwt_required
    def get(self, board_name):
        response = {
            "search_result": search_boards(board_name),
        }
        return response
