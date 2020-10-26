from flask_restx import Namespace, fields


class BoardDto:
    namespace = Namespace("board", description="Board operations")

    board_user = namespace.model("board_user", {
        "name": fields.String(required=True, description="user's name"),
        "user_id": fields.Integer(required=True, description="user's id"),
        "rank_icon": fields.Integer(required=True, description="number representing what rank icon to use"),
        "rank": fields.Integer(required=True, description="user's rank on this board"),
        "rating": fields.Float(required=True, description="user's Elo rating on this board"),
        "wins": fields.Integer(required=True, description="user's win count on this board"),
        "losses": fields.Integer(required=True, description="user's loss count on this board"),
    })

    board_profile_response = namespace.model("board_profile_response", {
        "board_id": fields.Integer(required=True, description="Id of the board being returned"),
        "board_name": fields.String(required=True, description="board's name"),
        "public": fields.Boolean(required=True, description="Whether or not this is a public board"),
        "member_count": fields.Integer(required=True, description="Number of board members"),
        "matches_count": fields.Integer(required=True, description="Number of verified matches on this board"),
        "top_members": fields.List(fields.Nested(board_user))
    })

    board_members_response = namespace.model("board_members_response", {
        "members": fields.List(fields.Nested(board_user))
    })

    board_match = namespace.model("board_match", {
        "submitter_name": fields.String(required=True, description="submitter's name"),
        "receiver_name": fields.String(required=True, description="receiver's name"),
        "submitter_result": fields.String(required=True, description="submitter's result of match {'Win', 'Loss', 'Draw'}"),
        "receiver_result": fields.String(required=True, description="receiver's result of match {'Win', 'Loss', 'Draw'}")
    })

    board_activity_response = namespace.model("board_activity_response", {
        "matches": fields.List(fields.Nested(board_match))
    })

    board_search = namespace.model("board_search", {
        "id": fields.Integer(required=True, description="Id of the board being returned"),
        "name": fields.String(required=True, description="Board's name"),
        "member_count": fields.Integer(required=True, description="Number of board members")
    })

    board_search_response = namespace.model("board_search_response", {
        "search_result": fields.List(fields.Nested(board_search))
    })

    create_board = namespace.model("create_board", {
        "board_name": fields.String(required=True, description="The name of the new board"),
        "public": fields.Boolean(required=True, description="Whether or not this is a public board")
    })

    create_board_response = namespace.model("create_board_response", {
        "success": fields.Boolean(required=True, description="Whether or not the board was successfully created"),
        "message": fields.String(required=True, description="Description of success or failure"),
        "board_id": fields.Integer(required=True, description="Id of the newly created board")
    })

    edit_board = namespace.model("edit_board", {
        "board_name": fields.String(required=True, description="The new name of the board"),
        "public": fields.Boolean(required=True, description="Whether or not this is a public board")
    })

    edit_board_response = namespace.model("edit_board_response", {
        "success": fields.Boolean(required=True, description="Whether or not the board was successfully edited"),
        "message": fields.String(required=True, description="Description of success or failure")
    })

    invite_to_board = namespace.model("invite_to_board", {
        "board_id": fields.Integer(required=True, description="The id of the board being invited to"),
        "user_id": fields.Integer(required=True, description="The id of the user being invited")
    })

    invite_to_board_response = namespace.model("invite_to_board_response", {
        "success": fields.Boolean(required=True, description="Whether or not the invite was successfully created"),
        "message": fields.String(required=True, description="Description of success or failure")
    })

    join_board = namespace.model("join_board", {
        "board_id": fields.Integer(required=True, description="The id of the board being joined"),
    })

    join_board_response = namespace.model("join_board_response", {
        "success": fields.Boolean(required=True, description="Whether or not the board was successfully joined"),
        "message": fields.String(required=True, description="Description of success or failure")
    })

    remove_from_board = namespace.model("remove_from_board", {
        "remove": fields.Boolean(required=True, description="Whether or not the user is being removed or just leaving\
                                                            {True = removing, False = leaving}"),
        "board_id": fields.Integer(required=True, description="The id of the board being left"),
        "user_id": fields.Integer(required=False, description="The id of the user being removed (needed if remove is True)")
    })

    remove_from_board_response = namespace.model("remove_from_board_response", {
        "success": fields.Boolean(required=True, description="Whether or not the leave/remove was successful"),
        "message": fields.String(required=True, description="Description of success or failure")
    })
