from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class ChecklistItemStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"


class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False, unique=True)
    scheme_code = Column(String(50), nullable=False)
    total_items = Column(Integer, default=0)
    compliant_items = Column(Integer, default=0)
    compliance_percentage = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    claim = relationship("Claim", back_populates="checklist")
    items = relationship("ChecklistItem", back_populates="checklist", lazy="select",
                         cascade="all, delete-orphan")


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(Integer, ForeignKey("checklists.id"), nullable=False, index=True)
    item_key = Column(String(100), nullable=False)
    item_label = Column(String(500), nullable=False)
    category = Column(String(100), nullable=True)
    is_mandatory = Column(Boolean, default=True)
    status = Column(SAEnum(ChecklistItemStatus, values_callable=lambda obj: [e.value for e in obj]), default=ChecklistItemStatus.PENDING)
    evidence_reference = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    verified_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    checklist = relationship("Checklist", back_populates="items")
