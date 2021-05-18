from fastapi import Header, HTTPException


async def get_auth_header(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(
            status_code=400, detail="Authorization header is None"
        )
    return authorization
