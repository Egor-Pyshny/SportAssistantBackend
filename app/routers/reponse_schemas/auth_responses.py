registration_responses = {
    409: {
        "description": "Conflict Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": {"message": "Email at the verification stage or already taken"}
                }
            }
        },
    },
    400: {
        "description": "Validation Error",
        "content": {
            "application/json": {"example": {"detail": {"message": "Wrong email or password"}}}
        },
    },
}
login_responses = {
    403: {
        "description": "Invalid credentials",
        "content": {
            "application/json": {"example": {"detail": {"message": "Wrong email or password"}}},
        },
    },
    400: {
        "description": "Validation Error",
        "content": {"application/json": {"example": {"detail": {"message": "Validation error"}}}},
    },
}
verification_responses = {
    404: {
        "description": "Email not found",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "Email is not in verification stage"}}
            },
        },
    },
    400: {
        "description": "Incorrect code or validation error",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "Verification code is expired"}}
            },
        },
    },
    429: {
        "description": "Too many requests",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "Too many requests, please try again later."}}
            }
        },
    },
}
resend_code_responses = {
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "User not in verification stage"}}
            }
        },
    },
    429: {
        "description": "Too many requests",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "Too many requests, please try again later."}}
            }
        },
    },
}
forgot_password_responses = {
    404: {
        "description": "User not found",
        "content": {"application/json": {"example": {"detail": {"message": "User not found"}}}},
    },
    429: {
        "description": "Too many requests",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "Too many requests, please try again later."}}
            }
        },
    },
    400: {
        "description": "Validation Error",
        "content": {"application/json": {"example": {"detail": {"message": "Validation error"}}}},
    },
}
reset_password_responses = {
    404: {
        "description": "User not found",
        "content": {"application/json": {"example": {"detail": {"message": "User not found"}}}},
    },
    400: {
        "description": "Validation Error",
        "content": {"application/json": {"example": {"detail": {"message": "Validation error"}}}},
    },
}
