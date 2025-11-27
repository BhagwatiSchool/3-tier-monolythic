from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ResourceResponse])
def get_user_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get resources - admin sees all, others see only finalized"""
    from app.models.user import UserRole
    
    if current_user.role == UserRole.admin:
        # Admin sees ALL their resources
        resources = db.query(Resource).filter(Resource.user_id == current_user.id).all()
    else:
        # Regular users see ONLY finalized resources
        resources = db.query(Resource).filter(
            Resource.user_id == current_user.id,
            Resource.is_finalized == True
        ).all()
    
    # Convert UUID to string for response
    return [
        ResourceResponse(
            id=r.id,
            user_id=str(r.user_id),
            icon=r.icon,
            title=r.title,
            resource_name=r.resource_name,
            description=r.description,
            status=r.status,
            region=r.region,
            is_finalized=r.is_finalized,
            created_at=r.created_at,
            updated_at=r.updated_at
        )
        for r in resources
    ]


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(
    resource_data: ResourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new resource for the current user"""
    resource = Resource(
        user_id=current_user.id,
        icon=resource_data.icon,
        title=resource_data.title,
        resource_name=resource_data.resource_name,
        description=resource_data.description,
        status=resource_data.status,
        region=resource_data.region
    )
    # Set custom created_at if provided
    if resource_data.created_at:
        resource.created_at = resource_data.created_at
    
    db.add(resource)
    db.commit()
    db.refresh(resource)
    
    # Convert UUID to string for response
    return ResourceResponse(
        id=resource.id,
        user_id=str(resource.user_id),
        icon=resource.icon,
        title=resource.title,
        resource_name=resource.resource_name,
        description=resource.description,
        status=resource.status,
        region=resource.region,
        is_finalized=resource.is_finalized,
        created_at=resource.created_at,
        updated_at=resource.updated_at
    )


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a resource (only if owned by current user)"""
    resource = db.query(Resource).filter(
        Resource.id == resource_id,
        Resource.user_id == current_user.id
    ).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or you don't have permission to update it"
        )
    
    resource.icon = resource_data.icon
    resource.title = resource_data.title
    resource.resource_name = resource_data.resource_name
    resource.description = resource_data.description
    resource.status = resource_data.status
    resource.region = resource_data.region
    
    # Update created_at if provided
    if resource_data.created_at:
        resource.created_at = resource_data.created_at
    
    db.commit()
    db.refresh(resource)
    
    # Convert UUID to string for response
    return ResourceResponse(
        id=resource.id,
        user_id=str(resource.user_id),
        icon=resource.icon,
        title=resource.title,
        resource_name=resource.resource_name,
        description=resource.description,
        status=resource.status,
        region=resource.region,
        is_finalized=resource.is_finalized,
        created_at=resource.created_at,
        updated_at=resource.updated_at
    )


@router.patch("/{resource_id}/finalize", response_model=ResourceResponse)
def finalize_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark resource as finalized (admin only)"""
    from app.models.user import UserRole
    
    # Only admin can finalize
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can finalize resources"
        )
    
    resource = db.query(Resource).filter(
        Resource.id == resource_id,
        Resource.user_id == current_user.id
    ).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    resource.is_finalized = True
    db.commit()
    db.refresh(resource)
    
    return ResourceResponse(
        id=resource.id,
        user_id=str(resource.user_id),
        icon=resource.icon,
        title=resource.title,
        resource_name=resource.resource_name,
        description=resource.description,
        status=resource.status,
        region=resource.region,
        is_finalized=resource.is_finalized,
        created_at=resource.created_at,
        updated_at=resource.updated_at
    )


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resource (only if owned by current user)"""
    resource = db.query(Resource).filter(
        Resource.id == resource_id,
        Resource.user_id == current_user.id
    ).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or you don't have permission to delete it"
        )
    
    db.delete(resource)
    db.commit()
    return None
