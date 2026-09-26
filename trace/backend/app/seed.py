"""
Seed script — populates DB with realistic demo data including flagged fraud cases.
Run with: python -m app.seed
"""
import asyncio
import hashlib
import random
import string
from datetime import datetime, date, timedelta
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.scheme import Scheme, SchemeCategory
from app.models.ngo import NGO, NGOStatus
from app.models.beneficiary import Beneficiary, BeneficiaryStatus
from app.models.claim import Claim, ClaimStatus
from app.models.invoice import Invoice, InvoiceStatus
from app.models.inspection import Inspection, InspectorAssignment, InspectionStatus, AssignmentStatus
from app.models.evidence import Evidence
from app.models.alert import Alert, AlertType, AlertSeverity, AlertStatus
from app.models.grievance import Grievance, GrievanceStatus, GrievanceCategory
from app.models.audit_log import AuditLog
from app.models.checklist import Checklist, ChecklistItem


def random_tracking_code():
    return "TRC-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


def sha256_hash(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


SCHEME_CHECKLISTS = {
    "SHRESTA": [
        {"key": "trainers_qualified", "label": "Trainers have required qualifications (ITI/Diploma)", "category": "Staffing"},
        {"key": "infra_workshop", "label": "Workshop with tools as per curriculum", "category": "Infrastructure"},
        {"key": "attendance_biometric", "label": "Biometric attendance system operational", "category": "Attendance"},
        {"key": "stipend_records", "label": "Stipend payment records maintained", "category": "Finance"},
        {"key": "tool_kits_distributed", "label": "Tool kits distributed to trainees", "category": "Materials"},
        {"key": "placement_records", "label": "Placement/job records maintained for graduates", "category": "Outcomes"},
        {"key": "meal_provided", "label": "Meals/refreshments provided as per norms", "category": "Welfare"},
        {"key": "insurance_enrolled", "label": "Trainees enrolled in accidental insurance", "category": "Welfare"},
    ],
    "PM-DAKSH": [
        {"key": "curriculum_approved", "label": "NSDC/Sector Skill Council approved curriculum used", "category": "Curriculum"},
        {"key": "assessment_agency", "label": "Assessment agency empanelled", "category": "Assessment"},
        {"key": "attendance_80pct", "label": "Minimum 80% attendance maintained by trainees", "category": "Attendance"},
        {"key": "digital_literacy", "label": "Digital literacy module included", "category": "Curriculum"},
        {"key": "bank_accounts_linked", "label": "Trainee bank accounts linked for stipend transfer", "category": "Finance"},
        {"key": "certificate_issuance", "label": "Certificates issued post-assessment", "category": "Assessment"},
    ],
    "NAMASTE": [
        {"key": "sanitation_workers_enrolled", "label": "Sanitation workers from hazardous occupations enrolled", "category": "Eligibility"},
        {"key": "ppe_provided", "label": "PPE (gloves, masks, boots) distributed and in use", "category": "Safety"},
        {"key": "health_checkup", "label": "Health screening conducted for all beneficiaries", "category": "Health"},
        {"key": "ppe_usage_cctv", "label": "CCTV confirms PPE usage during work", "category": "Safety"},
        {"key": "insurance_coverage", "label": "Workers enrolled in health insurance scheme", "category": "Welfare"},
        {"key": "sewage_safety_kit", "label": "Sewage safety kits in adequate quantity", "category": "Safety"},
    ],
    "SMILE": [
        {"key": "beneficiary_identity", "label": "Identity verification of transgender/destitute beneficiaries done", "category": "Eligibility"},
        {"key": "shelter_capacity", "label": "Shelter capacity matches claimed beneficiary count", "category": "Infrastructure"},
        {"key": "meal_quality", "label": "Meal quality meets minimum nutritional standards", "category": "Welfare"},
        {"key": "skill_training_ongoing", "label": "Skill training program actively running", "category": "Training"},
        {"key": "medical_aid", "label": "Medical assistance records maintained", "category": "Health"},
        {"key": "legal_aid", "label": "Legal aid access provided to beneficiaries", "category": "Legal"},
        {"key": "counseling", "label": "Counseling sessions conducted (records available)", "category": "Welfare"},
    ],
}


async def seed(db: AsyncSession):
    print("🌱 Seeding database...")

    # ─── IDEMPOTENCY GUARD ──────────────────────────────────────────────────
    result = await db.execute(text("SELECT COUNT(*) FROM schemes"))
    existing_count = result.scalar()
    if existing_count and existing_count > 0:
        print(f"✅ Database already seeded ({existing_count} schemes found) — skipping seed.")
        return

  
    # ─── SCHEMES ─────────────────────────────────────────────────────────────
    schemes_data = [
        {"name": "SHRESTA", "code": "SHRESTA", "description": "Scheme for Residential Education for Students in High schools in Targeted Areas — skill training for SC youth", "category": SchemeCategory.SCHEDULED_CASTE, "annual_budget_crore": 500},
        {"name": "PM-DAKSH", "code": "PM-DAKSH", "description": "PM-Dakshta Aur Kushalta Sampann Hitgrahi — upskilling of marginalized communities", "category": SchemeCategory.OBC, "annual_budget_crore": 350},
        {"name": "NAMASTE", "code": "NAMASTE", "description": "National Action for Mechanised Sanitation Ecosystem — safety of sanitation workers", "category": SchemeCategory.SCHEDULED_CASTE, "annual_budget_crore": 200},
        {"name": "SMILE", "code": "SMILE", "description": "Support for Marginalised Individuals for Livelihood and Enterprise — for transgender and beggars", "category": SchemeCategory.TRANSGENDER, "annual_budget_crore": 150},
    ]

    schemes = {}
    for sd in schemes_data:
        scheme = Scheme(
            name=sd["name"], code=sd["code"], description=sd["description"],
            category=sd["category"], annual_budget_crore=sd["annual_budget_crore"],
            checklist_template=SCHEME_CHECKLISTS.get(sd["code"], []),
            required_documents=["Registration Certificate", "Bank Details", "Beneficiary List", "Utilization Certificate"]
        )
        db.add(scheme)
    await db.flush()

    result = await db.execute(text("SELECT id, code FROM schemes"))
    for row in result:
        schemes[row.code] = row.id
    print(f"  ✓ {len(schemes)} schemes created")

    # ─── USERS ───────────────────────────────────────────────────────────────
    users_data = [
        {"email": "admin@trace.gov.in", "name": "System Administrator", "role": UserRole.SYSTEM_ADMIN, "password": "admin123"},
        {"email": "officer@dosje.gov.in", "name": "Dr. Priya Sharma", "role": UserRole.GOVT_OFFICER, "password": "officer123"},
        {"email": "officer2@dosje.gov.in", "name": "Rajesh Kumar", "role": UserRole.GOVT_OFFICER, "password": "officer123"},
        {"email": "inspector1@pmu.gov.in", "name": "Insp. Amit Verma", "role": UserRole.PMU_INSPECTOR, "password": "inspect123"},
        {"email": "inspector2@pmu.gov.in", "name": "Insp. Sunita Patel", "role": UserRole.PMU_INSPECTOR, "password": "inspect123"},
        {"email": "inspector3@pmu.gov.in", "name": "Insp. Mohan Rao", "role": UserRole.PMU_INSPECTOR, "password": "inspect123"},
        {"email": "inspector4@pmu.gov.in", "name": "Insp. Deepa Nair", "role": UserRole.PMU_INSPECTOR, "password": "inspect123"},
        {"email": "ngo1@janshiksha.org", "name": "Jan Shiksha Sansthan Admin", "role": UserRole.NGO_ADMIN, "password": "ngo123"},
        {"email": "ngo2@skillbridge.org", "name": "SkillBridge Foundation Admin", "role": UserRole.NGO_ADMIN, "password": "ngo123"},
        {"email": "ngo3@swachhindia.org", "name": "Swachh India Trust Admin", "role": UserRole.NGO_ADMIN, "password": "ngo123"},
        {"email": "ngo4@inclusive.org", "name": "Inclusive Lives NGO Admin", "role": UserRole.NGO_ADMIN, "password": "ngo123"},
        {"email": "beneficiary1@example.com", "name": "Ramesh Dalit", "role": UserRole.BENEFICIARY, "password": "bene123"},
        {"email": "beneficiary2@example.com", "name": "Sunita Bai", "role": UserRole.BENEFICIARY, "password": "bene123"},
    ]

    created_users = {}
    for ud in users_data:
        user = User(
            full_name=ud["name"], email=ud["email"],
            hashed_password=hash_password(ud["password"]),
            role=ud["role"], is_active=True, is_verified=True
        )
        db.add(user)
    await db.flush()

    result = await db.execute(text("SELECT id, email, role FROM users"))
    for row in result:
        created_users[row.email] = {"id": row.id, "role": row.role}
    print(f"  ✓ {len(created_users)} users created")

    # Update NGO admin user ngo_id after NGOs are created — done below

    # ─── NGOs ─────────────────────────────────────────────────────────────────
    ngos_data = [
        {
            "name": "Jan Shiksha Sansthan", "reg": "NGO/MH/2018/001234",
            "scheme": "SHRESTA", "district": "Pune", "state": "Maharashtra",
            "lat": 18.5204, "lng": 73.8567, "admin_email": "ngo1@janshiksha.org",
            "status": NGOStatus.APPROVED, "score": 88.5, "beneficiaries": 120, "has_cctv": True,
            "address": "45, Deccan Gymkhana, Pune, MH 411004"
        },
        {
            "name": "SkillBridge Foundation", "reg": "NGO/DL/2019/005678",
            "scheme": "PM-DAKSH", "district": "South Delhi", "state": "Delhi",
            "lat": 28.6139, "lng": 77.2090, "admin_email": "ngo2@skillbridge.org",
            "status": NGOStatus.APPROVED, "score": 42.0, "beneficiaries": 85, "has_cctv": True,
            "address": "12, Lajpat Nagar, New Delhi 110024"
        },
        {
            "name": "Swachh India Trust", "reg": "NGO/UP/2017/009012",
            "scheme": "NAMASTE", "district": "Lucknow", "state": "Uttar Pradesh",
            "lat": 26.8467, "lng": 80.9462, "admin_email": "ngo3@swachhindia.org",
            "status": NGOStatus.SUSPENDED, "score": 31.0, "beneficiaries": 200, "has_cctv": False,
            "address": "78, Hazratganj, Lucknow, UP 226001"
        },
        {
            "name": "Inclusive Lives Foundation", "reg": "NGO/KA/2020/003456",
            "scheme": "SMILE", "district": "Bengaluru Urban", "state": "Karnataka",
            "lat": 12.9716, "lng": 77.5946, "admin_email": "ngo4@inclusive.org",
            "status": NGOStatus.APPROVED, "score": 76.0, "beneficiaries": 60, "has_cctv": True,
            "address": "5, MG Road, Bengaluru, KA 560001"
        },
    ]

    ngo_ids = {}
    for nd in ngos_data:
        ngo = NGO(
            name=nd["name"], registration_number=nd["reg"],
            scheme_id=schemes[nd["scheme"]],
            address=nd["address"], district=nd["district"], state=nd["state"],
            latitude=nd["lat"], longitude=nd["lng"],
            location=f"SRID=4326;POINT({nd['lng']} {nd['lat']})",
            contact_person=nd["name"] + " Director",
            contact_email=nd["admin_email"],
            status=nd["status"], compliance_score=nd["score"],
            beneficiary_count_claimed=nd["beneficiaries"],
            has_cctv=nd["has_cctv"],
            cctv_feed_url=f"rtsp://mock-cctv.trace.local/{nd['reg'].replace('/', '-')}" if nd["has_cctv"] else None,
        )
        db.add(ngo)
    await db.flush()

    result = await db.execute(text("SELECT id, registration_number FROM ngos"))
    ngo_reg_map = {}
    for row in result:
        ngo_reg_map[row.registration_number] = row.id

    for nd in ngos_data:
        ngo_id = ngo_reg_map[nd["reg"]]
        ngo_ids[nd["name"]] = ngo_id
        # Update NGO admin user
        if nd["admin_email"] in created_users:
            uid = created_users[nd["admin_email"]]["id"]
            await db.execute(text(f"UPDATE users SET ngo_id = {ngo_id} WHERE id = {uid}"))

    print(f"  ✓ {len(ngo_ids)} NGOs created")

    # ─── BENEFICIARIES ────────────────────────────────────────────────────────
    bene_names_m = ["Raju Kumar", "Suresh Yadav", "Manoj Singh", "Vikram Prasad", "Deepak Joshi", "Arjun Meena", "Rakesh Rawat", "Dinesh Nayak"]
    bene_names_f = ["Savita Devi", "Rekha Patel", "Anita Kumari", "Priya Sharma", "Sunita Bai", "Kavita Rani", "Meena Devi", "Lata Chauhan"]

    all_bene_ids = {}
    for ngo_name, ngo_id in ngo_ids.items():
        count = ngos_data[[n["name"] for n in ngos_data].index(ngo_name)]["beneficiaries"]
        for i in range(min(count, 25)):  # seed up to 25 per NGO for brevity
            name = random.choice(bene_names_m + bene_names_f)
            is_dup = (i == 5 and ngo_name == "SkillBridge Foundation")  # fraud case
            is_ghost = (i == 10 and ngo_name == "Swachh India Trust")     # ghost case
            bene = Beneficiary(
                ngo_id=ngo_id,
                full_name=name + f" ({ngo_id}-{i})",
                aadhaar_hash=sha256_hash(f"dummy-aadhaar-{ngo_id}-{i}"),
                date_of_birth=date(1990 + (i % 25), (i % 12) + 1, (i % 28) + 1),
                gender="M" if name in bene_names_m else "F",
                category="SC" if ngo_name in ["Jan Shiksha Sansthan", "Swachh India Trust"] else "OBC",
                status=BeneficiaryStatus.DUPLICATE_FLAGGED if is_dup else
                       BeneficiaryStatus.GHOST_FLAGGED if is_ghost else
                       BeneficiaryStatus.ACTIVE,
                is_verified=not (is_dup or is_ghost),
                enrolled_date=datetime.now() - timedelta(days=random.randint(30, 180)),
                last_attendance_date=datetime.now() - timedelta(days=random.randint(0, 14)),
            )
            db.add(bene)

    await db.flush()
    print("  ✓ Beneficiaries seeded")

    # ─── CLAIMS ──────────────────────────────────────────────────────────────
    claim_ids = {}
    claims_data = [
        {"ngo": "Jan Shiksha Sansthan", "scheme": "SHRESTA", "amount": 1850000, "count": 120, "status": ClaimStatus.INSPECTION_DONE, "risk": 22.0},
        {"ngo": "SkillBridge Foundation", "scheme": "PM-DAKSH", "amount": 3200000, "count": 85, "status": ClaimStatus.UNDER_REVIEW, "risk": 78.5, "flags": ["Headcount mismatch detected", "Invoice price 45% above GeM rate"]},
        {"ngo": "Swachh India Trust", "scheme": "NAMASTE", "amount": 4100000, "count": 200, "status": ClaimStatus.INSPECTION_PENDING, "risk": 91.0, "flags": ["Ghost beneficiaries detected", "CCTV offline during inspection window", "Geo-spoofed evidence"]},
        {"ngo": "Inclusive Lives Foundation", "scheme": "SMILE", "amount": 980000, "count": 60, "status": ClaimStatus.APPROVED, "risk": 15.0},
    ]

    submitter_id = created_users["ngo1@janshiksha.org"]["id"]
    for i, cd in enumerate(claims_data):
        ngo_id = ngo_ids[cd["ngo"]]
        claim = Claim(
            ngo_id=ngo_id, scheme_id=schemes[cd["scheme"]],
            claim_period_start=datetime.now() - timedelta(days=90),
            claim_period_end=datetime.now() - timedelta(days=1),
            amount_claimed=cd["amount"],
            beneficiary_count_claimed=cd["count"],
            status=cd["status"],
            ai_risk_score=cd.get("risk", 0),
            ai_flags=cd.get("flags", []),
            description=f"Grant claim for {cd['scheme']} scheme — Q2 FY2025-26",
            submitted_by_user_id=submitter_id + i if (submitter_id + i) <= max(v["id"] for v in created_users.values()) else submitter_id,
        )
        db.add(claim)
    await db.flush()

    result = await db.execute(text("SELECT id, ngo_id FROM claims ORDER BY id"))
    claim_list = [{"id": row.id, "ngo_id": row.ngo_id} for row in result]
    for j, cd in enumerate(claims_data):
        if j < len(claim_list):
            claim_ids[cd["ngo"]] = claim_list[j]["id"]
    print(f"  ✓ {len(claim_list)} claims seeded")

    # ─── INSPECTIONS & ASSIGNMENTS ───────────────────────────────────────────
    inspector_ids = [v["id"] for k, v in created_users.items() if "inspector" in k]
    inspection_ids = {}

    for ngo_name, ngo_id in ngo_ids.items():
        cid = claim_ids.get(ngo_name)
        insp = Inspection(
            ngo_id=ngo_id, claim_id=cid,
            status=InspectionStatus.COMPLETED if ngo_name == "Jan Shiksha Sansthan" else
                   InspectionStatus.IN_PROGRESS if ngo_name == "SkillBridge Foundation" else
                   InspectionStatus.SCHEDULED,
            scheduled_at=datetime.now() - timedelta(days=7) if ngo_name == "Jan Shiksha Sansthan" else datetime.now() + timedelta(days=2),
            completed_at=datetime.now() - timedelta(days=5) if ngo_name == "Jan Shiksha Sansthan" else None,
            inspection_type="surprise", is_surprise=True,
            findings="Attendance records partially match. Minor discrepancies found in meal quality." if ngo_name == "Jan Shiksha Sansthan" else None,
            overall_score=74.0 if ngo_name == "Jan Shiksha Sansthan" else None,
        )
        db.add(insp)
    await db.flush()

    result = await db.execute(text("SELECT id, ngo_id FROM inspections ORDER BY id"))
    insp_list = [{"id": row.id, "ngo_id": row.ngo_id} for row in result]

    ngo_to_insp = {}
    for row in insp_list:
        for ngo_name, ngo_id in ngo_ids.items():
            if row["ngo_id"] == ngo_id:
                ngo_to_insp[ngo_name] = row["id"]

    # Assign inspectors (randomized)
    random.seed(42)  # Deterministic for seed
    for ngo_name, insp_id in ngo_to_insp.items():
        picked = random.choice(inspector_ids)
        assign = InspectorAssignment(
            inspection_id=insp_id, inspector_id=picked,
            status=AssignmentStatus.COMPLETED if ngo_name == "Jan Shiksha Sansthan" else AssignmentStatus.ACCEPTED,
            randomization_seed="seed-42-deterministic",
        )
        db.add(assign)
    await db.flush()
    print("  ✓ Inspections & assignments seeded")

    # ─── ALERTS ──────────────────────────────────────────────────────────────
    alerts_data = [
        {
            "ngo": "SkillBridge Foundation", "type": AlertType.HEADCOUNT_MISMATCH,
            "severity": AlertSeverity.HIGH, "status": AlertStatus.OPEN,
            "title": "Headcount Mismatch: 85 claimed vs 47 observed",
            "desc": "AI analysis of CCTV footage detected only 47 attendees against claimed 85. Variance: -44.7%",
            "details": {"claimed": 85, "observed": 47, "variance_pct": -44.7}
        },
        {
            "ngo": "SkillBridge Foundation", "type": AlertType.PRICE_OVERCHARGE,
            "severity": AlertSeverity.HIGH, "status": AlertStatus.INVESTIGATING,
            "title": "Invoice Price 45% Above GeM Rate",
            "desc": "OCR analysis of Invoice #SBF-2024-089 found training materials at ₹4,500/unit vs GeM rate of ₹3,100/unit",
            "details": {"item": "Training Kit Material Set", "our_price": 4500, "gem_price": 3100, "variance_pct": 45.2}
        },
        {
            "ngo": "Swachh India Trust", "type": AlertType.GHOST_BENEFICIARY,
            "severity": AlertSeverity.CRITICAL, "status": AlertStatus.OPEN,
            "title": "Ghost Beneficiary Alert: 23 unverifiable entries",
            "desc": "Facial recognition cross-check could not match 23 beneficiary photos with any real person in database. Possible ghost entries.",
            "details": {"total_claimed": 200, "unverifiable_count": 23, "percentage": 11.5}
        },
        {
            "ngo": "Swachh India Trust", "type": AlertType.GEO_SPOOF,
            "severity": AlertSeverity.CRITICAL, "status": AlertStatus.OPEN,
            "title": "Geo-Spoofing Detected in Evidence Submission",
            "desc": "EXIF GPS coordinates (Lucknow) do not match device network IP geolocation (Delhi). Evidence rejected.",
            "details": {"exif_location": "Lucknow, UP", "ip_location": "New Delhi", "distance_km": 520}
        },
        {
            "ngo": "Swachh India Trust", "type": AlertType.CCTV_OFFLINE,
            "severity": AlertSeverity.HIGH, "status": AlertStatus.OPEN,
            "title": "CCTV Feed Offline During Inspection Window",
            "desc": "CCTV feed was offline for 4.5 hours during the scheduled inspection window. Possibly deliberate.",
            "details": {"offline_duration_hours": 4.5, "inspection_window": "2026-09-20 10:00-15:00 IST"}
        },
        {
            "ngo": "Jan Shiksha Sansthan", "type": AlertType.DIETARY_SUBSTANDARD,
            "severity": AlertSeverity.MEDIUM, "status": AlertStatus.RESOLVED,
            "title": "Meal Quality Below Standard",
            "desc": "AI dietary scanner flagged meal as lacking adequate protein and vegetable portions in 3 photos.",
            "details": {"protein_score": 35, "vegetable_score": 40, "minimum_required": 60}
        },
    ]

    for ad in alerts_data:
        ngo_id = ngo_ids.get(ad["ngo"])
        alert = Alert(
            ngo_id=ngo_id, alert_type=ad["type"], severity=ad["severity"],
            status=ad["status"], title=ad["title"], description=ad["desc"],
            details=ad["details"],
            created_at=datetime.now() - timedelta(days=random.randint(1, 14))
        )
        db.add(alert)
    await db.flush()
    print(f"  ✓ {len(alerts_data)} alerts seeded")

    # ─── GRIEVANCES ───────────────────────────────────────────────────────────
    grievances_data = [
        {"ngo": "Swachh India Trust", "cat": GrievanceCategory.FOOD_QUALITY, "title": "खाना बहुत खराब है", "desc": "दोपहर का खाना ठंडा और बेस्वाद होता है, पर्याप्त मात्रा में नहीं दिया जा रहा", "lang": "hi", "anon": True},
        {"ngo": "SkillBridge Foundation", "cat": GrievanceCategory.ATTENDANCE_FRAUD, "title": "Fake attendance being marked", "desc": "Staff are marking attendance for people who are not present. I saw it happen 3 times.", "lang": "en", "anon": True},
        {"ngo": "Swachh India Trust", "cat": GrievanceCategory.STAFF_MISCONDUCT, "title": "Staff demanding bribe", "desc": "A staff member asked me for ₹500 to mark my attendance correctly.", "lang": "en", "anon": True},
        {"ngo": "Jan Shiksha Sansthan", "cat": GrievanceCategory.MISSING_SERVICES, "title": "Tool kits not provided", "desc": "We were told tool kits would be given but 2 months into training still nothing.", "lang": "en", "anon": False},
    ]

    for gd in grievances_data:
        ngo_id = ngo_ids.get(gd["ngo"])
        grievance = Grievance(
            ngo_id=ngo_id, is_anonymous=gd["anon"], category=gd["cat"],
            title=gd["title"], description=gd["desc"], language=gd["lang"],
            tracking_code=random_tracking_code(),
            status=GrievanceStatus.SUBMITTED,
        )
        db.add(grievance)
    await db.flush()
    print(f"  ✓ {len(grievances_data)} grievances seeded")

    # ─── CHECKLISTS ───────────────────────────────────────────────────────────
    for ngo_name, claim_id in claim_ids.items():
        scheme_code = next((nd["scheme"] for nd in ngos_data if nd["name"] == ngo_name), None)
        if not scheme_code:
            continue
        template = SCHEME_CHECKLISTS.get(scheme_code, [])
        checklist = Checklist(
            claim_id=claim_id, scheme_code=scheme_code,
            total_items=len(template)
        )
        db.add(checklist)
    await db.flush()

    result = await db.execute(text("SELECT id, claim_id FROM checklists"))
    cl_map = {row.claim_id: row.id for row in result}

    for ngo_name, claim_id in claim_ids.items():
        checklist_id = cl_map.get(claim_id)
        if not checklist_id:
            continue
        scheme_code = next((nd["scheme"] for nd in ngos_data if nd["name"] == ngo_name), None)
        template = SCHEME_CHECKLISTS.get(scheme_code, [])
        compliant = 0
        for t in template:
            is_ok = random.random() > 0.3 if ngo_name != "Swachh India Trust" else random.random() > 0.7
            status = "compliant" if is_ok else "non_compliant"
            if is_ok:
                compliant += 1
            item = ChecklistItem(
                checklist_id=checklist_id, item_key=t["key"],
                item_label=t["label"], category=t["category"],
                status=status, is_mandatory=True
            )
            db.add(item)
        await db.execute(text(
            f"UPDATE checklists SET compliant_items={compliant}, "
            f"compliance_percentage={int(compliant/len(template)*100)} WHERE id={checklist_id}"
        ))
    await db.flush()
    print("  ✓ Checklists seeded")

    await db.commit()
    print("✅ Database seeded successfully!")
    print("\n📋 Demo credentials:")
    for ud in users_data:
        print(f"   {ud['role'].value:20s}  {ud['email']:35s}  password: {ud['password']}")


async def main():
    async with AsyncSessionLocal() as session:
        await seed(session)


if __name__ == "__main__":
    asyncio.run(main())
