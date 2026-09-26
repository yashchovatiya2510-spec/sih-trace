from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, Enum as SAEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum
from app.core.database import Base


class NGOStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    SUSPENDED = "suspended"
    BLACKLISTED = "blacklisted"


class NGO(Base):
    __tablename__ = "ngos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(100), nullable=False, unique=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False, index=True)
    address = Column(Text, nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    # PostGIS point geometry: SRID 4326
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    contact_person = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    status = Column(SAEnum(NGOStatus), default=NGOStatus.PENDING, nullable=False, index=True)
    compliance_score = Column(Float, default=100.0)
    cctv_feed_url = Column(String(500), nullable=True)  # Real RTSP or mock URL
    has_cctv = Column(Boolean, default=False)
    beneficiary_count_claimed = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    scheme = relationship("Scheme", back_populates="ngos")
    beneficiaries = relationship("Beneficiary", back_populates="ngo", lazy="select")
    claims = relationship("Claim", back_populates="ngo", lazy="select")
    inspections = relationship("Inspection", back_populates="ngo", lazy="select")

    def __repr__(self):
        return f"<NGO {self.registration_number}: {self.name}>"
