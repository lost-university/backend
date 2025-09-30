import os

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/config")  # pragma: no cover
async def get_config() -> dict[str, str | None]:
    try:
        clerk_publishable_key = os.getenv("CLERK_PUBLISHABLE_KEY")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get config. Please report to page-admin") from e
    return {"clerkPublishableKey": clerk_publishable_key}
