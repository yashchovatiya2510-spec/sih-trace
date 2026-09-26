"""
AI Pipeline Package — T.R.A.C.E.

Real implementations:
- geo_check: Haversine geofencing (real)
- timestamp_check: EXIF timestamp validation (real)
- ocr_invoice: Tesseract OCR extraction (real)
- gem_price_compare: GeM price comparison (STUB — GeM API not publicly accessible)
- headcount_detect: YOLO-based headcount (STUB — real YOLO weights needed)
- face_recognition: Face deduplication (STUB — trained model needed)
- dietary_scan: Meal quality analysis (STUB — trained nutrition model needed)
"""
from app.ai.geo_check import check_geofence, validate_exif_timestamp
from app.ai.ocr import extract_invoice_data, compare_gem_prices
from app.ai.vision import detect_headcount, check_face_duplicates, analyze_meal_quality
from app.ai.randomizer import assign_inspector_randomly

__all__ = [
    "check_geofence", "validate_exif_timestamp",
    "extract_invoice_data", "compare_gem_prices",
    "detect_headcount", "check_face_duplicates", "analyze_meal_quality",
    "assign_inspector_randomly"
]
