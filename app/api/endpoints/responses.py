LOGIN = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "first_name": "Firstname",
                    "last_name": "Lastname",
                    "other_name": "Othername",
                    "email": "example@example.com",
                    "phone": "+381000000000",
                    "birthday": "1905-05-19",
                    "is_admin": False,
                }
            }
        }
    }
}

LOGOUT = {
    200: {
        "description": "Successful Response",
        "content": {"status": "OK"},
    }
}

USERS_CURRENT = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "first_name": "Firstname",
                    "last_name": "Lastname",
                    "other_name": "Othername",
                    "email": "example@example.com",
                    "phone": "+381000000000",
                    "birthday": "1905-05-19",
                    "is_admin": False,
                }
            }
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}

USERS_EDIT = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "id": 0,
                    "first_name": "Firstname",
                    "last_name": "Lastname",
                    "other_name": "Othername",
                    "email": "example@example.com",
                    "phone": "+381000000000",
                    "birthday": "1905-05-19",
                }
            }
        },
    },
    400: {
        "description": "Bad request",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}

USERS = {
    200: {
        "description": "Successful Response",
        "content": {
            "data": [
                {
                    "id": 2,
                    "first_name": "Firstname",
                    "last_name": "Lastname",
                    "email": "example@example.com",
                },
            ],
            "meta": {"pagination": {"total": 1, "page": 1, "size": 2}},
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}

PRIVATE_USERS = {
    200: {
        "description": "Successful Response",
        "content": {
            "data": [
                {
                    "id": 0,
                    "first_name": "Firstname",
                    "last_name": "Lastname",
                    "email": "example@example.com",
                }
            ],
            "meta": {
                "pagination": {"total": 2, "page": 2, "size": 1},
                "hint": {"city": [{"id": 2, "name": "Cityname"}]},
            },
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    403: {
        "description": "Forbidden",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}

PRIVATE_USERS_POST = {
    201: {
        "description": "Successful Response",
        "content": {
            "id": 2,
            "first_name": "string",
            "last_name": "string",
            "other_name": "string",
            "email": "string@gmail.com",
            "phone": "string",
            "birthday": "2023-05-19",
            "is_admin": True,
            "city": 0,
            "additional_info": "string",
        },
    },
    400: {
        "description": "Bad request",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    403: {
        "description": "Forbidden",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}

PRIVATE_USERS_PK = {
    200: {
        "description": "Successful Response",
        "content": {
            "id": 2,
            "first_name": "string",
            "last_name": "string",
            "other_name": "string",
            "email": "string@gmail.com",
            "phone": "string",
            "birthday": "2023-05-19",
            "is_admin": True,
            "city": 0,
            "additional_info": "string",
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    403: {
        "description": "Forbidden",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    404: {
        "description": "Not found",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}

PRIVATE_DELETE = {
    204: {
        "description": "Successful Response",
        "content": {},
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    403: {
        "description": "Forbidden",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    404: {
        "description": "Not found",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}

PRIVATE_UPDATE = {
    200: {
        "description": "Successful Response",
        "content": {
            "id": 3,
            "first_name": "string",
            "last_name": "string",
            "other_name": "string",
            "email": "string33@gmail.com",
            "phone": "+12345678654",
            "birthday": "2023-05-10",
            "is_admin": False,
            "city": 1,
            "additional_info": "add info",
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    403: {
        "description": "Forbidden",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
    404: {
        "description": "Not found",
        "content": {"application/json": {"example": {"detail": "detail"}}},
    },
}
