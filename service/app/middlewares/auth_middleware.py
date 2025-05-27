import os
from typing import Annotated

from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import AuthenticateRequestOptions, RequestState
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from sqlmodel import Session

from ..database import get_session
from ..services.user_service import create_user, get_user_by_clerk_id

load_dotenv()


async def auth_dependency(request: Request, session: Annotated[Session, Depends(get_session)]) -> RequestState:
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

    request_state = sdk.authenticate_request(
        request, AuthenticateRequestOptions(authorized_parties=os.getenv("AUTHORIZED_PARTIES").split(","))
    )

    if not request_state.is_signed_in:
        raise HTTPException(status_code=401, detail="Unauthorized")

    request.state.user = get_user_by_clerk_id(request_state.payload["sub"], session)

    if request.state.user is not None:
        return request_state

    sdk_user = sdk.users.get(user_id=request_state.payload["sub"])

    if sdk_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    request.state.user = create_user(request_state.payload["sub"], sdk_user.email_addresses[0].email_address, session)

    return request_state
