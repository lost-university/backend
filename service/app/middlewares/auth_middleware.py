import os

from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import AuthenticateRequestOptions, RequestState
from fastapi import HTTPException, Request
from sqlmodel import Session, select

from ..database import engine
from ..models.user import User


def auth_dependency(request: Request) -> RequestState:
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

    request_state = sdk.authenticate_request(
        request, AuthenticateRequestOptions(authorized_parties=["http://localhost:5173"])
    )

    if not request_state.is_signed_in:
        raise HTTPException(status_code=401, detail="Unauthorized")

    with Session(engine) as session:
        statement = select(User).where(User.clerk_id == request_state.payload["sub"])
        request.state.user = session.exec(statement).first()

        if request.state.user is not None:
            return request_state

        sdk_user = sdk.users.get(user_id=request_state.payload["sub"])

        if sdk_user is None:
            raise HTTPException(status_code=401, detail="User not found")

        request.state.user = User(
            clerk_id=request_state.payload["sub"], email=sdk_user.email_addresses[0].email_address
        )
        session.add(request.state.user)
        session.commit()

    return request_state
