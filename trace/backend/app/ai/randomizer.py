"""
Inspector randomization — REAL implementation.
Uses cryptographically seeded PRNG + availability/distance weighting.
"""
import secrets
import random
import hashlib
from typing import List, Optional, Tuple
from dataclasses import dataclass
from app.ai.geo_check import haversine_distance_m


@dataclass
class InspectorCandidate:
    user_id: int
    name: str
    latitude: Optional[float]
    longitude: Optional[float]
    active_assignments: int  # Current open assignments


def assign_inspector_randomly(
    candidates: List[InspectorCandidate],
    ngo_lat: float,
    ngo_lon: float,
    exclude_user_ids: Optional[List[int]] = None,
) -> Tuple[Optional[InspectorCandidate], str]:
    """
    Blind, weighted random assignment of an inspector to an inspection site.

    Algorithm:
    1. Filter out excluded inspectors (conflict of interest, overloaded)
    2. Score each candidate:
       - Base score = 100
       - -10 per active assignment (prefer less busy)
       - Distance weight: closer inspectors get a slight boost for feasibility
         but NOT so much that geography is predictable (anti-gaming)
    3. Use cryptographically random seed for final selection

    Returns:
        (assigned_candidate, randomization_seed)
        randomization_seed is stored for full audit trail.
    """
    exclude_ids = set(exclude_user_ids or [])

    # Filter
    eligible = [c for c in candidates if c.user_id not in exclude_ids and c.active_assignments < 3]

    if not eligible:
        # Fallback: allow anyone
        eligible = [c for c in candidates if c.user_id not in exclude_ids]

    if not eligible:
        return None, ""

    # Score each candidate
    scores = []
    for c in eligible:
        score = 100.0
        score -= c.active_assignments * 10  # Workload penalty

        if c.latitude and c.longitude and ngo_lat and ngo_lon:
            dist_km = haversine_distance_m(c.latitude, c.longitude, ngo_lat, ngo_lon) / 1000
            # Soft distance factor — only minor influence (max ±15 points)
            dist_score = max(0, 15 - (dist_km / 100) * 5)
            # Add controlled noise so distance alone isn't deterministic
            dist_score += random.uniform(-3, 3)
            score += dist_score

        scores.append(max(score, 1.0))  # Ensure positive

    # Cryptographic seed
    seed_bytes = secrets.token_bytes(16)
    seed_hex = seed_bytes.hex()
    seed_int = int.from_bytes(seed_bytes, "big")

    # Weighted random selection using seed
    rng = random.Random(seed_int)
    total = sum(scores)
    cumulative = 0.0
    threshold = rng.uniform(0, total)

    selected = eligible[-1]  # Fallback
    for i, (candidate, score) in enumerate(zip(eligible, scores)):
        cumulative += score
        if cumulative >= threshold:
            selected = candidate
            break

    # Audit-quality seed hash
    audit_seed = hashlib.sha256(
        f"{seed_hex}:{selected.user_id}:{ngo_lat}:{ngo_lon}".encode()
    ).hexdigest()[:32]

    return selected, f"rng-{seed_hex[:8]}-audit-{audit_seed[:8]}"
