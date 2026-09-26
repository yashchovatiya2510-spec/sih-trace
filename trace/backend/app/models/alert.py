from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SAEnum, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(str, enum.Enum):
    GHOST_BENEFICIARY = "ghost_beneficiary"
    DUPLICATE_BENEFICIARY = "duplicate_beneficiary"
    HEADCOUNT_MISMATCH = "headcount_mismatch"
    PRICE_OVERCHARGE = "price_overcharge"
    GEO_SPOOF = "geo_spoof"
    TIMESTAMP_SPOOF = "timestamp_spoof"
    DIETARY_SUBSTANDARD = "dietary_substandard"
    INSPECTION_MISSED = "inspection_missed"
    SUSPICIOUS_CLAIM = "suspicious_claim"
    CCTV_OFFLINE = "cctv_offline"


class AlertStatus(str, enum.Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(Integer, ForeignKey("ngos.id"), nullable=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=True)
    evidence_id = Column(Integer, ForeignKey("evidence.id"), nullable=True)
    alert_type = Column(SAEnum(AlertType, values_callable=lambda obj: [e.value for e in obj]), nullable=False, index=True)
    severity = Column(SAEnum(AlertSeverity, values_callable=lambda obj: [e.value for e in obj]), nullable=False, index=True)
    status = Column(SAEnum(AlertStatus, values_callable=lambda obj: [e.value for e in obj]), default=AlertStatus.OPEN, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)  # Additional structured data
    acknowledged_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<Alert {self.alert_type} severity={self.severity} ngo={self.ngo_id}>"
