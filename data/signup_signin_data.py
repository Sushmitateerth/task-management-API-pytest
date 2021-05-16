from http import HTTPStatus

negative_cases = [
    (
        "signup",
        {"username": "user", "password": "Pa!2"},
        HTTPStatus.BAD_REQUEST,
        "password must be longer than or equal to 8 characters"
    ),
    (
        "signup",
        {"username": "usertest1", "password": ""},
        HTTPStatus.BAD_REQUEST,
        [
            'password must contain 1 uppercase, 1 lowercase and 1 number or special character',
            'password must be longer than or equal to 8 characters'
        ]
    ),
    (
        "signin",
        {"username": "incorrect user", "password": "passwrd1@"},
        HTTPStatus.UNAUTHORIZED,
        "Unauthorized"
    ),
    (
        "signin",
        {"username": "test2 user", "password": "passwrd1@"},
        HTTPStatus.UNAUTHORIZED,
        "Unauthorized"
    ),
    (
        "signin",
        {"username": "test2 user", "password": ""},
        HTTPStatus.BAD_REQUEST,
        "password should not be empty"
    ),
    (
        "signin",
        {"username": "", "password": "passwrd1@"},
        HTTPStatus.BAD_REQUEST,
        "username should not be empty"
    ),
]

user_conflict_case = [
    (
        {"username": "test2 user", "password": "Passw0rd!"},
        HTTPStatus.CONFLICT,
        "username test2 user already exists"
    )
]

positive_case = [
    (
        {"username": "test2 user", "password": "Passw0rd!"}
    )
]
