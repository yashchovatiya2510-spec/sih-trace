from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SAEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class GrievanceStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    CLOSED = "closed"


class GrievanceCategory(str, enum.Enum):
    FOOD_QUALITY = "food_quality"
    MISSING_SERVICES = "missing_services"
    STAFF_MISCONDUCT = "staff_misconduct"
    ATTENDANCE_FRAUD = "attendance_fraud"
    FINANCIAL_IRREGULARITY = "financial_irregularity"
    FACILITY_ISSUE = "facility_issue"
    OTHER = "other"


class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(Integer, ForeignKey("ngos.id"), nullable=False, index=True)
    beneficiary_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NULL = anonymous
    is_anonymous = Column(Boolean, default=True)
    category = Column(SAEnum(GrievanceCategory), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    language = Column(String(10), default="en")  # en | hi
    status = Column(SAEnum(GrievanceStatus), default=GrievanceStatus.SUBMITTED, index=True)
    tracking_code = Column(String(20), unique=True, nullable=False)  # Public tracking code
    response = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    beneficiary_user = relationship("User", back_populates="grievances")

    def __repr__(self):
        return f"<Grievance {self.tracking_code}: {self.category}>"
