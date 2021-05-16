from http import HTTPStatus

positive_case = [
    (
        {"title": "test board"},
        HTTPStatus.CREATED
    )
]

negative_case = [
    (
        {
            "title": "",
            "description": "None",
            "participants": [
                0
            ]
        },
        HTTPStatus.BAD_REQUEST,
        "title should not be empty"
    ),
]


