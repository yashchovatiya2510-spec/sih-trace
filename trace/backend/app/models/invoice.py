from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum as SAEnum, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class InvoiceStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    OCR_PROCESSING = "ocr_processing"
    OCR_DONE = "ocr_done"
    PRICE_CHECKED = "price_checked"
    FLAGGED = "flagged"
    CLEARED = "cleared"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False, index=True)
    vendor_name = Column(String(255), nullable=True)
    invoice_number = Column(String(100), nullable=True)
    invoice_date = Column(DateTime(timezone=True), nullable=True)
    total_amount = Column(Float, nullable=True)
    file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    status = Column(SAEnum(InvoiceStatus), default=InvoiceStatus.UPLOADED, index=True)

    # OCR extracted data
    ocr_raw_text = Column(Text, nullable=True)
    ocr_line_items = Column(JSON, nullable=True)  # [{item, qty, unit_price, total}]

    # GeM price comparison (STUB — GeM API not accessible)
    # *** STUB: gem_price_data is populated from mock data. Replace with real GeM API call. ***
    gem_comparison = Column(JSON, nullable=True)  # [{item, our_price, gem_price, variance_pct}]
    price_flag_count = Column(Integer, default=0)
    max_price_variance_pct = Column(Float, nullable=True)
    is_price_flagged = Column(Boolean, default=False)

    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    claim = relationship("Claim", back_populates="invoices")

    def __repr__(self):
        return f"<Invoice {self.invoice_number}: Claim={self.claim_id}>"
