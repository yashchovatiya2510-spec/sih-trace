from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.core.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False, index=True)
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=True)  # photo | video | document
    file_size_bytes = Column(Integer, nullable=True)

    # Geo metadata — immutable after upload
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)
    location_accuracy_meters = Column(Float, nullable=True)

    # Timestamp integrity
    captured_at = Column(DateTime(timezone=True), nullable=True)   # From EXIF / device
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())  # Server-set, immutable
    exif_data = Column(JSON, nullable=True)

    # Anti-spoofing checks
    geo_check_passed = Column(Boolean, nullable=True)     # Within geofence of NGO
    timestamp_check_passed = Column(Boolean, nullable=True)  # EXIF within ±30min of upload
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(Text, nullable=True)

    # AI analysis results (set by AI pipeline)
    ai_head_count = Column(Integer, nullable=True)
    ai_head_count_claimed = Column(Integer, nullable=True)
    ai_dietary_score = Column(Float, nullable=True)  # 0-100
    ai_analysis_raw = Column(JSON, nullable=True)

    # Relationships
    inspection = relationship("Inspection", back_populates="evidence_items")

    def __repr__(self):
        return f"<Evidence {self.id}: Inspection={self.inspection_id}>"
