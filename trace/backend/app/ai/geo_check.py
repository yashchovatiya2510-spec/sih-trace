"""
Geo-fencing and timestamp validation — REAL implementations.
Uses Haversine formula for distance calculation.
"""
import math
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
import json


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great-circle distance between two GPS points in meters.
    Uses the Haversine formula — accurate to within 0.5%.
    """
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def check_geofence(
    evidence_lat: float,
    evidence_lon: float,
    ngo_lat: float,
    ngo_lon: float,
    radius_meters: float = 500.0,
) -> Tuple[bool, float, str]:
    """
    Check whether captured evidence GPS is within the allowed radius of the NGO site.

    Returns:
        (passed: bool, distance_m: float, reason: str)
    """
    if evidence_lat is None or evidence_lon is None:
        return False, -1.0, "No GPS coordinates in evidence"
    if ngo_lat is None or ngo_lon is None:
        return False, -1.0, "NGO location not configured"

    distance = haversine_distance_m(evidence_lat, evidence_lon, ngo_lat, ngo_lon)

    if distance <= radius_meters:
        return True, distance, f"Within geofence ({distance:.1f}m from site, limit {radius_meters}m)"
    else:
        return False, distance, (
            f"GEO-SPOOF ALERT: Evidence captured {distance:.0f}m from NGO site "
            f"(allowed radius: {radius_meters}m)"
        )


def validate_exif_timestamp(
    exif_data: Optional[dict],
    upload_time: Optional[datetime] = None,
    max_delta_minutes: int = 30,
) -> Tuple[bool, str]:
    """
    Validate that EXIF timestamp is close to upload time (anti-spoofing).
    Rejects photos with stale or future-dated timestamps.

    Returns:
        (passed: bool, reason: str)
    """
    if upload_time is None:
        upload_time = datetime.now(timezone.utc)

    if not exif_data:
        return False, "No EXIF data present — photo metadata stripped (suspicious)"

    exif_dt_str = exif_data.get("DateTimeOriginal") or exif_data.get("DateTime")
    if not exif_dt_str:
        return False, "EXIF timestamp field missing"

    # Try parsing common EXIF date formats
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            exif_dt = datetime.strptime(exif_dt_str, fmt)
            if exif_dt.tzinfo is None:
                exif_dt = exif_dt.replace(tzinfo=timezone.utc)
            break
        except ValueError:
            exif_dt = None

    if exif_dt is None:
        return False, f"Could not parse EXIF timestamp: {exif_dt_str}"

    delta = abs((upload_time - exif_dt).total_seconds() / 60)

    if exif_dt > upload_time + timedelta(minutes=5):
        return False, f"TIMESTAMP SPOOF: Photo dated {(exif_dt - upload_time).seconds // 60}min in the future"
    elif delta > max_delta_minutes:
        return False, (
            f"STALE PHOTO: EXIF timestamp is {delta:.0f} minutes from upload time "
            f"(max allowed: {max_delta_minutes}min). Photo may have been pre-captured."
        )
    else:
        return True, f"Timestamp valid — {delta:.1f} min difference from upload time"
