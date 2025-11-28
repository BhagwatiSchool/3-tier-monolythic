from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class ResourceStatus(str):
    RUNNING = "Running"
    STOPPED = "Stopped"
    PENDING = "Pending"


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(100), nullable=False)
    resource_name = Column(String(200), nullable=False)
    description = Column(String(500))
    status = Column(String(20), default=ResourceStatus.RUNNING)
    region = Column(String(50), default="East US")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="resources")
