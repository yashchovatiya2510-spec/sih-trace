"""
Invoice OCR and GeM Price Comparison.

OCR: REAL — uses Tesseract via pytesseract + OpenCV preprocessing.
GeM Price Compare: *** STUB *** — GeM portal API is not publicly accessible.
                   Architecture is correct; replace _fetch_gem_prices() with real API call.
"""
import re
import os
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


# ─── MOCK GeM PRICE DATABASE ─────────────────────────────────────────────────
# *** STUB: This represents GeM portal price data. Replace with real GeM API calls. ***
_GEM_MOCK_PRICES: Dict[str, float] = {
    "training kit": 3100.0,
    "training kit material set": 3100.0,
    "laptop": 35000.0,
    "projector": 22000.0,
    "whiteboard": 4500.0,
    "chair": 1200.0,
    "desk": 3500.0,
    "uniform": 650.0,
    "ppe kit": 850.0,
    "safety gloves": 120.0,
    "safety boots": 900.0,
    "mask n95": 45.0,
    "first aid kit": 1200.0,
    "stationery set": 250.0,
    "textbook": 350.0,
    "notebook": 45.0,
    "pen": 12.0,
    "calculator": 450.0,
    "tiffin box": 180.0,
    "water bottle": 150.0,
}


def _preprocess_image_for_ocr(image_path: str) -> Optional["np.ndarray"]:
    """Preprocess image for better OCR accuracy."""
    if not TESSERACT_AVAILABLE:
        return None
    img = cv2.imread(image_path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Deskew, denoise, threshold
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Scale up small images for better OCR
    h, w = thresh.shape
    if w < 800:
        scale = 800 / w
        thresh = cv2.resize(thresh, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_LINEAR)
    return thresh


def _parse_line_items_from_text(raw_text: str) -> List[Dict]:
    """
    Parse invoice line items from OCR raw text.
    Looks for patterns: [item name] [quantity] [unit price] [total]
    Returns structured list of items.
    """
    lines = raw_text.split("\n")
    items = []

    # Pattern: text followed by numbers (qty, price, total)
    price_pattern = re.compile(
        r"^(.+?)\s+(\d+(?:\.\d+)?)\s+[\₹Rs\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+[\₹Rs\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)$"
    )
    simple_pattern = re.compile(
        r"^(.+?)\s+[\₹Rs\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)$"
    )

    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue
        m = price_pattern.match(line)
        if m:
            try:
                items.append({
                    "item": m.group(1).strip(),
                    "qty": float(m.group(2).replace(",", "")),
                    "unit_price": float(m.group(3).replace(",", "")),
                    "total": float(m.group(4).replace(",", "")),
                })
                continue
            except ValueError:
                pass
        m = simple_pattern.match(line)
        if m and any(k in line.lower() for k in ["kit", "laptop", "chair", "uniform", "training", "book", "notebook"]):
            try:
                items.append({
                    "item": m.group(1).strip(),
                    "qty": 1,
                    "unit_price": float(m.group(2).replace(",", "")),
                    "total": float(m.group(2).replace(",", "")),
                })
            except ValueError:
                pass

    return items


def extract_invoice_data(file_path: str) -> Dict:
    """
    Extract structured data from an invoice image using Tesseract OCR.
    REAL implementation — requires tesseract-ocr installed.
    """
    result = {
        "raw_text": "",
        "vendor_name": None,
        "invoice_number": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": [],
        "ocr_confidence": 0.0,
        "error": None,
    }

    if not TESSERACT_AVAILABLE:
        result["error"] = "Tesseract not installed — OCR unavailable"
        # Return mock data for demo purposes
        result["raw_text"] = "INVOICE\nSkillBridge Supplies Pvt Ltd\nInvoice #SBF-2024-089\nDate: 15/09/2026\nTraining Kit Material Set  15  4500.00  67500.00\nTextbooks  85  420.00  35700.00\nNotebooks  85  55.00  4675.00\nTOTAL: ₹107875.00"
        result["line_items"] = [
            {"item": "Training Kit Material Set", "qty": 15, "unit_price": 4500.0, "total": 67500.0},
            {"item": "Textbooks", "qty": 85, "unit_price": 420.0, "total": 35700.0},
            {"item": "Notebooks", "qty": 85, "unit_price": 55.0, "total": 4675.0},
        ]
        result["vendor_name"] = "SkillBridge Supplies Pvt Ltd"
        result["invoice_number"] = "SBF-2024-089"
        result["total_amount"] = 107875.0
        return result

    if not os.path.exists(file_path):
        result["error"] = f"File not found: {file_path}"
        return result

    try:
        preprocessed = _preprocess_image_for_ocr(file_path)
        if preprocessed is not None:
            pil_img = Image.fromarray(preprocessed)
        else:
            pil_img = Image.open(file_path)

        raw_text = pytesseract.image_to_string(pil_img, lang="eng", config="--psm 6")
        result["raw_text"] = raw_text

        # Extract vendor name (usually in first 3 lines)
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        if lines:
            result["vendor_name"] = lines[0][:100]

        # Invoice number
        inv_match = re.search(r"(?:invoice|inv|bill)\s*[#no:.]*\s*([A-Z0-9\-/]+)", raw_text, re.I)
        if inv_match:
            result["invoice_number"] = inv_match.group(1)

        # Date
        date_match = re.search(r"(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})", raw_text)
        if date_match:
            result["invoice_date"] = date_match.group(1)

        # Total amount
        total_match = re.search(r"(?:total|grand total|amount)[:\s₹Rs.]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", raw_text, re.I)
        if total_match:
            result["total_amount"] = float(total_match.group(1).replace(",", ""))

        # Line items
        result["line_items"] = _parse_line_items_from_text(raw_text)

    except Exception as e:
        result["error"] = str(e)

    return result


def compare_gem_prices(line_items: List[Dict]) -> Tuple[List[Dict], int, float]:
    """
    Compare invoice line items against GeM portal prices.

    *** STUB: GeM portal API (https://gem.gov.in) is not publicly accessible.
    _fetch_gem_prices() uses a hardcoded mock price table.
    To make real: replace _GEM_MOCK_PRICES with live API call to GeM catalog. ***

    Args:
        line_items: List of {item, qty, unit_price, total}

    Returns:
        (comparison_results, flag_count, max_variance_pct)
    """
    results = []
    flag_count = 0
    max_variance = 0.0

    for item in line_items:
        item_name = item.get("item", "").lower().strip()
        our_price = float(item.get("unit_price", 0))

        # Fuzzy match against mock GeM prices
        gem_price = None
        for gem_item, price in _GEM_MOCK_PRICES.items():
            if gem_item in item_name or any(word in item_name for word in gem_item.split()):
                gem_price = price
                break

        if gem_price is None or our_price == 0:
            results.append({
                "item": item.get("item"),
                "our_price": our_price,
                "gem_price": None,
                "variance_pct": None,
                "flagged": False,
                "note": "No GeM listing found for comparison",
            })
            continue

        variance_pct = ((our_price - gem_price) / gem_price) * 100

        flagged = variance_pct > 15.0  # Flag if >15% above GeM price
        if flagged:
            flag_count += 1
        if variance_pct > max_variance:
            max_variance = variance_pct

        results.append({
            "item": item.get("item"),
            "our_price": our_price,
            "gem_price": gem_price,
            "variance_pct": round(variance_pct, 2),
            "flagged": flagged,
            "note": f"{'⚠ OVERPRICED by ' + str(round(variance_pct, 1)) + '%' if flagged else '✓ Within acceptable range'}",
        })

    return results, flag_count, max_variance
