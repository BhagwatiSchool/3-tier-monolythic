from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.db.database import get_db
from app.models.user import ThemeConfig, User
from app.api.deps import get_current_admin_user, get_current_user

router = APIRouter()


@router.get("/")
def get_user_theme(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user-specific theme"""
    config = db.query(ThemeConfig).filter(ThemeConfig.user_id == current_user.id).first()
    
    if config and config.theme_data:
        return json.loads(config.theme_data)
    
    return {"mode": "light", "colorScheme": "blue"}


@router.put("/")
def save_user_theme(
    theme_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save user-specific theme"""
    config = db.query(ThemeConfig).filter(ThemeConfig.user_id == current_user.id).first()
    
    theme_json = json.dumps(theme_data)
    
    if not config:
        config = ThemeConfig(
            user_id=current_user.id,
            theme_data=theme_json
        )
        db.add(config)
    else:
        config.theme_data = theme_json
    
    db.commit()
    db.refresh(config)
    return theme_data
