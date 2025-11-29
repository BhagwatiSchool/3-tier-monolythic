from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.db.database import get_db
from app.schemas.user import ThemeConfigResponse, ThemeConfigUpdate
from app.models.user import ThemeConfig, User
from app.api.deps import get_current_admin_user, get_current_user

router = APIRouter()


@router.get("/")
def get_user_theme(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = str(current_user.id)
    config_key = f"user_theme_{user_id}"
    print(f"🔍 GET theme: user_id={user_id}, config_key={config_key}")
    
    config = db.query(ThemeConfig).filter(ThemeConfig.config_key == config_key).first()
    
    if config and config.config_value:
        try:
            theme_data = json.loads(config.config_value)
            print(f"✅ Loaded theme for user {user_id}: {theme_data}")
            return theme_data
        except json.JSONDecodeError:
            print(f"❌ Failed to parse theme for user {user_id}")
            return {}
    
    print(f"ℹ️ No theme found for user {user_id}")
    return {}


@router.put("/")
def save_user_theme(
    theme_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = str(current_user.id)
    config_key = f"user_theme_{user_id}"
    
    theme_json = json.dumps(theme_data)
    print(f"\n✅ PUT theme: user_id={user_id}, config_key={config_key}")
    print(f"   Data: {theme_data}")
    print(f"   JSON: {theme_json}")
    
    config = db.query(ThemeConfig).filter(ThemeConfig.config_key == config_key).first()
    
    if not config:
        config = ThemeConfig(
            config_key=config_key,
            config_value=theme_json
        )
        db.add(config)
        print(f"   ➕ Created NEW theme record")
    else:
        print(f"   ♻️ Updated existing theme record")
        config.config_value = theme_json
    
    try:
        db.commit()
        db.refresh(config)
        print(f"   ✅ Committed to database successfully")
    except Exception as e:
        print(f"   ❌ Database commit failed: {str(e)}")
        db.rollback()
        raise
    
    return theme_data


@router.get("/all", response_model=List[ThemeConfigResponse])
def get_all_theme_configs(
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    configs = db.query(ThemeConfig).all()
    return configs


@router.patch("/{config_key}", response_model=ThemeConfigResponse)
def update_theme_config(
    config_key: str,
    config_update: ThemeConfigUpdate,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    config = db.query(ThemeConfig).filter(ThemeConfig.config_key == config_key).first()
    
    if not config:
        # Create if doesn't exist
        config = ThemeConfig(
            config_key=config_key,
            config_value=config_update.config_value
        )
        db.add(config)
    else:
        config.config_value = config_update.config_value
    
    db.commit()
    db.refresh(config)
    return config
