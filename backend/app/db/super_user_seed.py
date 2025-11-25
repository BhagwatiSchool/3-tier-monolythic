from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.security import get_password_hash


def create_super_user(db: Session) -> None:
    """Create main admin user (protected) if it doesn't exist"""
    admin_email = "ritesh@apka.bhai"
    
    # Check if admin user already exists
    existing_user = db.query(User).filter(User.email == admin_email).first()
    
    if not existing_user:
        # Create protected admin user with default password
        admin_user = User(
            email=admin_email,
            hashed_password=get_password_hash("Aagebadho"),
            display_name="Ritesh - Admin",
            role=UserRole.admin,
            is_protected=True  # Mark as protected super admin
        )
        db.add(admin_user)
        db.commit()
        print(f"✅ Protected admin user created: {admin_email}")
    else:
        # Ensure existing user has admin role and is_protected flag
        needs_update = False
        if existing_user.role != UserRole.admin:
            existing_user.role = UserRole.admin
            needs_update = True
        if not existing_user.is_protected:
            existing_user.is_protected = True
            needs_update = True
        
        if needs_update:
            db.commit()
            print(f"✅ Updated user to protected admin: {admin_email}")
        else:
            print(f"ℹ️  Protected admin user already exists: {admin_email}")
