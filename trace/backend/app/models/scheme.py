from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum as SAEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class SchemeCategory(str, enum.Enum):
    SCHEDULED_CASTE = "scheduled_caste"
    SCHEDULED_TRIBE = "scheduled_tribe"
    OBC = "obc"
    WOMEN = "women"
    DISABILITY = "disability"
    SENIOR_CITIZEN = "senior_citizen"
    TRANSGENDER = "transgender"
    DENOTIFIED_TRIBES = "denotified_tribes"


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    category = Column(SAEnum(SchemeCategory), nullable=False)
    ministry = Column(String(255), default="Ministry of Social Justice & Empowerment")
    annual_budget_crore = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    checklist_template = Column(JSON, nullable=True)  # JSON array of checklist items
    required_documents = Column(JSON, nullable=True)   # JSON array of required doc names
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    claims = relationship("Claim", back_populates="scheme", lazy="select")
    ngos = relationship("NGO", back_populates="scheme", lazy="select")

    def __repr__(self):
        return f"<Scheme {self.code}: {self.name}>"
