from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    GOVT_OFFICER = "govt_officer"
    PMU_INSPECTOR = "pmu_inspector"
    NGO_ADMIN = "ngo_admin"
    BENEFICIARY = "beneficiary"
    SYSTEM_ADMIN = "system_admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    ngo_id = Column(Integer, nullable=True)  # FK set at app level to avoid circular
    preferred_language = Column(String(10), default="en")
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user", lazy="select")
    assignments = relationship("InspectorAssignment", back_populates="inspector", lazy="select",
                               foreign_keys="InspectorAssignment.inspector_id")
    grievances = relationship("Grievance", back_populates="beneficiary_user", lazy="select")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
