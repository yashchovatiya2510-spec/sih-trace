from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum as SAEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class ClaimStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INSPECTION_PENDING = "inspection_pending"
    INSPECTION_DONE = "inspection_done"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(Integer, ForeignKey("ngos.id"), nullable=False, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False, index=True)
    claim_period_start = Column(DateTime(timezone=True), nullable=True)
    claim_period_end = Column(DateTime(timezone=True), nullable=True)
    amount_claimed = Column(Float, nullable=False)
    amount_approved = Column(Float, nullable=True)
    beneficiary_count_claimed = Column(Integer, nullable=False)
    beneficiary_count_verified = Column(Integer, nullable=True)
    status = Column(SAEnum(ClaimStatus), default=ClaimStatus.DRAFT, nullable=False, index=True)
    description = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    submitted_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ai_risk_score = Column(Float, nullable=True)  # 0-100, higher = more risky
    ai_flags = Column(JSON, nullable=True)         # List of AI-detected issues
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    ngo = relationship("NGO", back_populates="claims")
    scheme = relationship("Scheme", back_populates="claims")
    invoices = relationship("Invoice", back_populates="claim", lazy="select")
    inspections = relationship("Inspection", back_populates="claim", lazy="select")
    checklist = relationship("Checklist", back_populates="claim", uselist=False, lazy="select")

    def __repr__(self):
        return f"<Claim {self.id}: NGO={self.ngo_id} Status={self.status}>"
