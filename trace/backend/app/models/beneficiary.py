from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class BeneficiaryStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DUPLICATE_FLAGGED = "duplicate_flagged"
    GHOST_FLAGGED = "ghost_flagged"


class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(Integer, ForeignKey("ngos.id"), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    aadhaar_hash = Column(String(64), nullable=True)  # SHA-256 of Aadhaar — NOT plain Aadhaar
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    category = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    face_encoding_path = Column(String(500), nullable=True)  # Path to stored face encoding
    status = Column(SAEnum(BeneficiaryStatus), default=BeneficiaryStatus.ACTIVE, index=True)
    is_verified = Column(Boolean, default=False)
    enrolled_date = Column(DateTime(timezone=True), nullable=True)
    last_attendance_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    ngo = relationship("NGO", back_populates="beneficiaries")

    def __repr__(self):
        return f"<Beneficiary {self.id}: {self.full_name}>"
