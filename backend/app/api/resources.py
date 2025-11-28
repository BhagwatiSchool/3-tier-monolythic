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
    
    # Convert to response model
    return [
        ResourceResponse(
            id=r.id,
            user_id=str(r.user_id),
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
    
    # Convert to response model
    return ResourceResponse(
        id=resource.id,
        user_id=str(resource.user_id),
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
    
    # Convert to response model
    return ResourceResponse(
        id=resource.id,
        user_id=str(resource.user_id),
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
    
    # Template resources - Azure specific (12 resources)
    templates = [
        {
            "title": "Azure Virtual Machine",
            "resource_name": "vm-prod-eastus-01",
            "description": "Windows/Linux VM for compute workloads",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure App Service",
            "resource_name": "app-service-api-prod",
            "description": "Managed web app hosting",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure SQL Database",
            "resource_name": "sqldb-prod-eastus",
            "description": "Managed relational database",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Cosmos DB",
            "resource_name": "cosmosdb-main",
            "description": "NoSQL distributed database",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Storage Account",
            "resource_name": "stgacct-prod-eastus",
            "description": "Blob, Table, Queue storage",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Key Vault",
            "resource_name": "keyvault-prod-eastus",
            "description": "Secrets and certificate management",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Load Balancer",
            "resource_name": "lb-frontend-prod",
            "description": "Network load balancing",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure API Management",
            "resource_name": "apim-prod-eastus",
            "description": "API gateway and management",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Container Registry",
            "resource_name": "acr-prod-eastus",
            "description": "Docker container image repository",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Functions",
            "resource_name": "func-app-serverless",
            "description": "Serverless compute functions",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Service Bus",
            "resource_name": "servicebus-prod",
            "description": "Message queuing and pub/sub",
            "status": "Running",
            "region": "East US"
        },
        {
            "title": "Azure Application Insights",
            "resource_name": "appinsights-prod",
            "description": "Application monitoring and analytics",
            "status": "Running",
            "region": "East US"
        }
    ]
    
    created_resources = []
    for template in templates:
        resource = Resource(
            user_id=current_user.id,
            title=template["title"],
            resource_name=template["resource_name"],
            description=template["description"],
            status=template["status"],
            region=template["region"]
        )
        db.add(resource)
        db.flush()
        
        created_resources.append(ResourceResponse(
            id=resource.id,
            user_id=str(resource.user_id),
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
