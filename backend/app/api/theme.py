from fastapi import APIRouter, Depends
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/")
def get_user_theme(current_user: User = Depends(get_current_user)):
    """Get user theme - stored in localStorage on frontend"""
    return {"mode": "light", "colorScheme": "blue"}


@router.put("/")
def save_user_theme(theme_data: dict, current_user: User = Depends(get_current_user)):
    """Save theme - handled by frontend localStorage, backend just acknowledges"""
    return theme_data
