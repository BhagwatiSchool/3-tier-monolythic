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
    """Get all resources - admin sees their own, others see admin's resources"""
    from app.models.user import UserRole
    
    if current_user.role == UserRole.admin:
        # Admin sees their own resources
        resources = db.query(Resource).filter(Resource.user_id == current_user.id).all()
    else:
        # Regular users see the admin's resources
        admin = db.query(User).filter(User.role == UserRole.admin).first()
        if admin:
            resources = db.query(Resource).filter(Resource.user_id == admin.id).all()
        else:
            resources = []
    
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
    """Create a new resource - admin only"""
    from app.models.user import UserRole
    
    # Only admin can create resources
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create resources"
        )
    
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
    """Update a resource - admin only"""
    from app.models.user import UserRole
    
    # Only admin can update resources
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update resources"
        )
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
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
        created_at=resource.created_at,
        updated_at=resource.updated_at
    )




@router.post("/seed/templates", response_model=List[ResourceResponse], status_code=status.HTTP_201_CREATED)
def seed_template_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Seed default template resources - admin only"""
    from app.models.user import UserRole
    
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can seed resources"
        )
    
    # Template resources
    templates = [
        {
            "title": "Web Server",
            "resource_name": "nginx-prod-01",
            "description": "Production nginx web server",
            "icon": "server",
            "status": "Running",
            "region": "us-east-1"
        },
        {
            "title": "Database",
            "resource_name": "postgres-db-01",
            "description": "Primary PostgreSQL database",
            "icon": "database",
            "status": "Running",
            "region": "us-east-1"
        },
        {
            "title": "Cache Server",
            "resource_name": "redis-cache-01",
            "description": "Redis caching layer",
            "icon": "zap",
            "status": "Running",
            "region": "us-east-1"
        },
        {
            "title": "Load Balancer",
            "resource_name": "lb-prod-01",
            "description": "Application load balancer",
            "icon": "network",
            "status": "Running",
            "region": "us-east-1"
        },
        {
            "title": "Storage",
            "resource_name": "s3-bucket-main",
            "description": "Main S3 storage bucket",
            "icon": "hard_drive",
            "status": "Running",
            "region": "us-east-1"
        },
        {
            "title": "API Gateway",
            "resource_name": "api-gateway-01",
            "description": "REST API gateway",
            "icon": "link",
            "status": "Running",
            "region": "us-east-1"
        }
    ]
    
    created_resources = []
    for template in templates:
        resource = Resource(
            user_id=current_user.id,
            title=template["title"],
            resource_name=template["resource_name"],
            description=template["description"],
            icon=template["icon"],
            status=template["status"],
            region=template["region"]
        )
        db.add(resource)
        db.flush()
        
        created_resources.append(ResourceResponse(
            id=resource.id,
            user_id=str(resource.user_id),
            icon=resource.icon,
            title=resource.title,
            resource_name=resource.resource_name,
            description=resource.description,
            status=resource.status,
            region=resource.region,
            created_at=resource.created_at,
            updated_at=resource.updated_at
        ))
    
    db.commit()
    return created_resources


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resource - admin only"""
    from app.models.user import UserRole
    
    # Only admin can delete resources
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete resources"
        )
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    db.delete(resource)
    db.commit()
    return None
