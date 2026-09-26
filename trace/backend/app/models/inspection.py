from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum as SAEnum, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum
from app.core.database import Base


class InspectionStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    NOTIFIED = "notified"
    IN_PROGRESS = "in_progress"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    COMPLETED = "completed"
    MISSED = "missed"
    CANCELLED = "cancelled"


class AssignmentStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DECLINED = "declined"


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(Integer, ForeignKey("ngos.id"), nullable=False, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True, index=True)
    status = Column(SAEnum(InspectionStatus), default=InspectionStatus.SCHEDULED, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    inspection_type = Column(String(50), default="surprise")  # surprise | routine | video_call
    findings = Column(Text, nullable=True)
    overall_score = Column(Float, nullable=True)  # 0-100
    is_surprise = Column(Boolean, default=True)
    video_call_session_id = Column(String(255), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    ngo = relationship("NGO", back_populates="inspections")
    claim = relationship("Claim", back_populates="inspections")
    assignments = relationship("InspectorAssignment", back_populates="inspection", lazy="select")
    evidence_items = relationship("Evidence", back_populates="inspection", lazy="select")


class InspectorAssignment(Base):
    __tablename__ = "inspector_assignments"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False, index=True)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(SAEnum(AssignmentStatus), default=AssignmentStatus.PENDING, index=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    randomization_seed = Column(String(100), nullable=True)  # Record the seed used for audit trail
    notes = Column(Text, nullable=True)

    # Relationships
    inspection = relationship("Inspection", back_populates="assignments")
    inspector = relationship("User", back_populates="assignments", foreign_keys=[inspector_id])

    def __repr__(self):
        return f"<Assignment Inspection={self.inspection_id} Inspector={self.inspector_id}>"
