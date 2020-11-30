from flask_restx import Namespace, fields


class UserDto:
    namespace = Namespace("user", description="User operations")

    register_user = namespace.model(
        "register_user",
        {
            "email": fields.String(required=True, description="User's email address"),
            "name": fields.String(required=True, description="User's username"),
            "password": fields.String(required=True, description="User's password in plaintext"),
        },
    )

    register_user_response = namespace.model(
        "register_user_response",
        {
            "success": fields.Boolean(required=True, description="Whether or not the user was successfully created"),
            "message": fields.String(required=True, description="Description of success or failure"),
            "access_token": fields.String(description="JWT access token"),
            "user_id": fields.Integer(description="The user's id"),
        },
    )

    user_board = namespace.model(
        "user_board",
        {
            "board_name": fields.String(required=True, description="board's name"),
            "board_id": fields.Integer(required=True, description="board's id"),
            "rank_icon": fields.Integer(required=True, description="number representing what rank icon to use"),
            "rank": fields.Integer(required=True, description="user's rank on this board"),
            "users_count": fields.Integer(required=True, description="count of users on this board"),
            "rating": fields.Float(required=True, description="user's Elo rating on this board"),
            "wins": fields.Integer(required=True, description="user's win count on this board"),
            "losses": fields.Integer(required=True, description="user's loss count on this board"),
        },
    )

    user_profile_response = namespace.model(
        "user_profile_response",
        {
            "user_id": fields.Integer(required=True, description="Id of the user being returned"),
            "name": fields.String(required=True, description="User's username"),
            "board_count": fields.Integer(
                required=True, description="Number of boards the user is an active member of"
            ),
            "matches_count": fields.Integer(
                required=True, description="Number of verified matches the user was part of"
            ),
            "favourite_boards": fields.List(fields.Nested(user_board)),
        },
    )

    user_boards_response = namespace.model("user_boards_response", {"boards": fields.List(fields.Nested(user_board))})

    user_match = namespace.model(
        "user_match",
        {
            "board_name": fields.String(required=True, description="board's name"),
            "opponent_name": fields.String(required=True, description="opponent's name"),
            "rating_change": fields.Float(required=True, description="change in user's elo from this match"),
            "result": fields.String(required=True, description="result of match {'Win', 'Loss', 'Draw'}"),
        },
    )

    user_activity_response = namespace.model(
        "user_activity_response", {"matches": fields.List(fields.Nested(user_match))}
    )

    user_search = namespace.model(
        "user_search",
        {
            "id": fields.Integer(required=True, description="Id of the user being returned"),
            "name": fields.String(required=True, description="User's username"),
            "board_count": fields.Integer(
                required=True, description="Number of boards the user is an active member of"
            ),
        },
    )

    user_search_response = namespace.model(
        "user_search_response", {"search_result": fields.List(fields.Nested(user_search))}
    )

    favourite_board = namespace.model(
        "favourite_board",
        {
            "add_favourite": fields.Boolean(
                required=True,
                description="Whether or not the board is being added or removed from favourites\
                                                                    {True = add, False = remove}",
            ),
            "board_id": fields.Integer(required=True, description="the id of the board to add/remove from favourites"),
        },
    )

    favourite_board_response = namespace.model(
        "favourite_board_response",
        {
            "success": fields.Boolean(
                required=True, description="Whether or not the board was successfully added/removed to/from favourites"
            ),
            "message": fields.String(required=True, description="Description of success or failure"),
        },
    )
