from fastapi import Header


def get_jwt_user(authorization: str = Header(...)) -> UserID:
    """
    Pretend this function gets a UserID from a JWT in the auth header
    """
    return authorization
