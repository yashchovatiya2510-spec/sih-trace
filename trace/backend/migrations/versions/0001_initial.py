"""Initial schema with PostGIS

Revision ID: 0001_initial
Revises: 
Create Date: 2026-09-25
"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('govt_officer', 'pmu_inspector', 'ngo_admin', 'beneficiary', 'system_admin', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('ngo_id', sa.Integer(), nullable=True),
        sa.Column('preferred_language', sa.String(10), nullable=True, server_default='en'),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Schemes table
    op.create_table(
        'schemes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Enum('scheduled_caste', 'scheduled_tribe', 'obc', 'women', 'disability', 'senior_citizen', 'transgender', 'denotified_tribes', name='schemecategory'), nullable=False),
        sa.Column('ministry', sa.String(255), nullable=True),
        sa.Column('annual_budget_crore', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('checklist_template', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('required_documents', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('code'),
    )
    op.create_index('ix_schemes_code', 'schemes', ['code'])

    # NGOs table
    op.create_table(
        'ngos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('registration_number', sa.String(100), nullable=False),
        sa.Column('scheme_id', sa.Integer(), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('district', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('pincode', sa.String(10), nullable=True),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('contact_person', sa.String(255), nullable=True),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('contact_phone', sa.String(20), nullable=True),
        sa.Column('status', sa.Enum('pending', 'approved', 'suspended', 'blacklisted', name='ngostatus'), nullable=False, server_default='pending'),
        sa.Column('compliance_score', sa.Float(), nullable=True, server_default='100.0'),
        sa.Column('cctv_feed_url', sa.String(500), nullable=True),
        sa.Column('has_cctv', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('beneficiary_count_claimed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['scheme_id'], ['schemes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('registration_number'),
    )
    op.create_index('ix_ngos_id', 'ngos', ['id'])
    op.create_index('ix_ngos_scheme_id', 'ngos', ['scheme_id'])
    op.create_index('ix_ngos_status', 'ngos', ['status'])

    # Beneficiaries table
    op.create_table(
        'beneficiaries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ngo_id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('aadhaar_hash', sa.String(64), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(20), nullable=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('face_encoding_path', sa.String(500), nullable=True),
        sa.Column('status', sa.Enum('active', 'inactive', 'duplicate_flagged', 'ghost_flagged', name='beneficiarystatus'), nullable=True, server_default='active'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('enrolled_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_attendance_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['ngo_id'], ['ngos.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_beneficiaries_ngo_id', 'beneficiaries', ['ngo_id'])

    # Claims table
    op.create_table(
        'claims',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ngo_id', sa.Integer(), nullable=False),
        sa.Column('scheme_id', sa.Integer(), nullable=False),
        sa.Column('claim_period_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('claim_period_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('amount_claimed', sa.Float(), nullable=False),
        sa.Column('amount_approved', sa.Float(), nullable=True),
        sa.Column('beneficiary_count_claimed', sa.Integer(), nullable=False),
        sa.Column('beneficiary_count_verified', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('draft', 'submitted', 'under_review', 'inspection_pending', 'inspection_done', 'approved', 'rejected', 'disbursed', name='claimstatus'), nullable=False, server_default='draft'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('submitted_by_user_id', sa.Integer(), nullable=True),
        sa.Column('reviewed_by_user_id', sa.Integer(), nullable=True),
        sa.Column('ai_risk_score', sa.Float(), nullable=True),
        sa.Column('ai_flags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['ngo_id'], ['ngos.id']),
        sa.ForeignKeyConstraint(['scheme_id'], ['schemes.id']),
        sa.ForeignKeyConstraint(['submitted_by_user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['reviewed_by_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_claims_ngo_id', 'claims', ['ngo_id'])
    op.create_index('ix_claims_scheme_id', 'claims', ['scheme_id'])
    op.create_index('ix_claims_status', 'claims', ['status'])
    op.create_index('ix_claims_created_at', 'claims', ['created_at'])

    # Invoices table
    op.create_table(
        'invoices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('claim_id', sa.Integer(), nullable=False),
        sa.Column('vendor_name', sa.String(255), nullable=True),
        sa.Column('invoice_number', sa.String(100), nullable=True),
        sa.Column('invoice_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=True),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('original_filename', sa.String(255), nullable=True),
        sa.Column('status', sa.Enum('uploaded', 'ocr_processing', 'ocr_done', 'price_checked', 'flagged', 'cleared', name='invoicestatus'), nullable=True, server_default='uploaded'),
        sa.Column('ocr_raw_text', sa.Text(), nullable=True),
        sa.Column('ocr_line_items', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('gem_comparison', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('price_flag_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('max_price_variance_pct', sa.Float(), nullable=True),
        sa.Column('is_price_flagged', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('uploaded_by_user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['claim_id'], ['claims.id']),
        sa.ForeignKeyConstraint(['uploaded_by_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_invoices_claim_id', 'invoices', ['claim_id'])

    # Inspections table
    op.create_table(
        'inspections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ngo_id', sa.Integer(), nullable=False),
        sa.Column('claim_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('scheduled', 'notified', 'in_progress', 'evidence_submitted', 'completed', 'missed', 'cancelled', name='inspectionstatus'), nullable=True, server_default='scheduled'),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('inspection_type', sa.String(50), nullable=True, server_default='surprise'),
        sa.Column('findings', sa.Text(), nullable=True),
        sa.Column('overall_score', sa.Float(), nullable=True),
        sa.Column('is_surprise', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('video_call_session_id', sa.String(255), nullable=True),
        sa.Column('created_by_user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['ngo_id'], ['ngos.id']),
        sa.ForeignKeyConstraint(['claim_id'], ['claims.id']),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_inspections_ngo_id', 'inspections', ['ngo_id'])
    op.create_index('ix_inspections_status', 'inspections', ['status'])

    # Inspector Assignments
    op.create_table(
        'inspector_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('inspection_id', sa.Integer(), nullable=False),
        sa.Column('inspector_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'accepted', 'in_progress', 'completed', 'declined', name='assignmentstatus'), nullable=True, server_default='pending'),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('randomization_seed', sa.String(100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['inspection_id'], ['inspections.id']),
        sa.ForeignKeyConstraint(['inspector_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_inspector_assignments_inspection_id', 'inspector_assignments', ['inspection_id'])
    op.create_index('ix_inspector_assignments_inspector_id', 'inspector_assignments', ['inspector_id'])

    # Evidence table
    op.create_table(
        'evidence',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('inspection_id', sa.Integer(), nullable=False),
        sa.Column('uploaded_by_user_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('original_filename', sa.String(255), nullable=True),
        sa.Column('file_type', sa.String(50), nullable=True),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('location_accuracy_meters', sa.Float(), nullable=True),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('exif_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('geo_check_passed', sa.Boolean(), nullable=True),
        sa.Column('timestamp_check_passed', sa.Boolean(), nullable=True),
        sa.Column('is_flagged', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('flag_reason', sa.Text(), nullable=True),
        sa.Column('ai_head_count', sa.Integer(), nullable=True),
        sa.Column('ai_head_count_claimed', sa.Integer(), nullable=True),
        sa.Column('ai_dietary_score', sa.Float(), nullable=True),
        sa.Column('ai_analysis_raw', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['inspection_id'], ['inspections.id']),
        sa.ForeignKeyConstraint(['uploaded_by_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_evidence_inspection_id', 'evidence', ['inspection_id'])

    # Alerts
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ngo_id', sa.Integer(), nullable=True),
        sa.Column('claim_id', sa.Integer(), nullable=True),
        sa.Column('inspection_id', sa.Integer(), nullable=True),
        sa.Column('evidence_id', sa.Integer(), nullable=True),
        sa.Column('alert_type', sa.Enum('ghost_beneficiary', 'duplicate_beneficiary', 'headcount_mismatch', 'price_overcharge', 'geo_spoof', 'timestamp_spoof', 'dietary_substandard', 'inspection_missed', 'suspicious_claim', 'cctv_offline', name='alerttype'), nullable=False),
        sa.Column('severity', sa.Enum('low', 'medium', 'high', 'critical', name='alertseverity'), nullable=False),
        sa.Column('status', sa.Enum('open', 'acknowledged', 'investigating', 'resolved', 'false_positive', name='alertstatus'), nullable=True, server_default='open'),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('acknowledged_by_user_id', sa.Integer(), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['ngo_id'], ['ngos.id']),
        sa.ForeignKeyConstraint(['claim_id'], ['claims.id']),
        sa.ForeignKeyConstraint(['inspection_id'], ['inspections.id']),
        sa.ForeignKeyConstraint(['evidence_id'], ['evidence.id']),
        sa.ForeignKeyConstraint(['acknowledged_by_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_alerts_ngo_id', 'alerts', ['ngo_id'])
    op.create_index('ix_alerts_alert_type', 'alerts', ['alert_type'])
    op.create_index('ix_alerts_severity', 'alerts', ['severity'])
    op.create_index('ix_alerts_status', 'alerts', ['status'])
    op.create_index('ix_alerts_created_at', 'alerts', ['created_at'])

    # Grievances
    op.create_table(
        'grievances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ngo_id', sa.Integer(), nullable=False),
        sa.Column('beneficiary_user_id', sa.Integer(), nullable=True),
        sa.Column('is_anonymous', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('category', sa.Enum('food_quality', 'missing_services', 'staff_misconduct', 'attendance_fraud', 'financial_irregularity', 'facility_issue', 'other', name='grievancecategory'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('language', sa.String(10), nullable=True, server_default='en'),
        sa.Column('status', sa.Enum('submitted', 'under_review', 'resolved', 'closed', name='grievancestatus'), nullable=True, server_default='submitted'),
        sa.Column('tracking_code', sa.String(20), nullable=False),
        sa.Column('response', sa.Text(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['ngo_id'], ['ngos.id']),
        sa.ForeignKeyConstraint(['beneficiary_user_id'], ['users.id']),
        sa.UniqueConstraint('tracking_code'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_grievances_ngo_id', 'grievances', ['ngo_id'])
    op.create_index('ix_grievances_status', 'grievances', ['status'])

    # Checklists
    op.create_table(
        'checklists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('claim_id', sa.Integer(), nullable=False),
        sa.Column('scheme_code', sa.String(50), nullable=False),
        sa.Column('total_items', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('compliant_items', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('compliance_percentage', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['claim_id'], ['claims.id']),
        sa.UniqueConstraint('claim_id'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'checklist_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('checklist_id', sa.Integer(), nullable=False),
        sa.Column('item_key', sa.String(100), nullable=False),
        sa.Column('item_label', sa.String(500), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('is_mandatory', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('status', sa.Enum('pending', 'compliant', 'non_compliant', 'not_applicable', name='checklistitemstatus'), nullable=True, server_default='pending'),
        sa.Column('evidence_reference', sa.String(500), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('verified_by_user_id', sa.Integer(), nullable=True),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['checklist_id'], ['checklists.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['verified_by_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_checklist_items_checklist_id', 'checklist_items', ['checklist_id'])

    # Audit Logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(255), nullable=False),
        sa.Column('resource_type', sa.String(100), nullable=True),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'])


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('checklist_items')
    op.drop_table('checklists')
    op.drop_table('grievances')
    op.drop_table('alerts')
    op.drop_table('evidence')
    op.drop_table('inspector_assignments')
    op.drop_table('inspections')
    op.drop_table('invoices')
    op.drop_table('claims')
    op.drop_table('beneficiaries')
    op.drop_table('ngos')
    op.drop_table('schemes')
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS schemecategory")
    op.execute("DROP TYPE IF EXISTS ngostatus")
    op.execute("DROP TYPE IF EXISTS beneficiarystatus")
    op.execute("DROP TYPE IF EXISTS claimstatus")
    op.execute("DROP TYPE IF EXISTS invoicestatus")
    op.execute("DROP TYPE IF EXISTS inspectionstatus")
    op.execute("DROP TYPE IF EXISTS assignmentstatus")
    op.execute("DROP TYPE IF EXISTS alerttype")
    op.execute("DROP TYPE IF EXISTS alertseverity")
    op.execute("DROP TYPE IF EXISTS alertstatus")
    op.execute("DROP TYPE IF EXISTS grievancecategory")
    op.execute("DROP TYPE IF EXISTS grievancestatus")
    op.execute("DROP TYPE IF EXISTS checklistitemstatus")
