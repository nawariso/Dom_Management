"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dorms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=512), nullable=False),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.UniqueConstraint("name", name="uq_dorm_name"),
    )

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("dorm_id", sa.Integer(), sa.ForeignKey("dorms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.UniqueConstraint("dorm_id", "name", name="uq_building_name_per_dorm"),
    )

    op.create_table(
        "floors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.UniqueConstraint("building_id", "number", name="uq_floor_number_per_building"),
    )

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("floor_id", sa.Integer(), sa.ForeignKey("floors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("number", sa.String(length=50), nullable=False),
        sa.Column("is_occupied", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.UniqueConstraint("floor_id", "number", name="uq_room_number_per_floor"),
    )

    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("move_in", sa.Date(), nullable=True),
        sa.Column("move_out", sa.Date(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.UniqueConstraint("email", name="uq_tenant_email"),
    )

    op.create_table(
        "tariffs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("rate_per_unit", sa.Numeric(10, 4), nullable=False),
        sa.Column("base_fee", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="THB"),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("tiers", sa.JSON(), nullable=True),
        sa.UniqueConstraint("name", name="uq_tariff_name"),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_name", sa.String(length=255), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("interval", sa.String(length=50), nullable=False),
        sa.Column("next_billing_date", sa.Date(), nullable=False),
        sa.Column("status", sa.Enum("active", "past_due", "canceled", "paused", name="subscription_status"), nullable=False),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )

    op.create_table(
        "meters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("serial_number", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.UniqueConstraint("serial_number", name="uq_meter_serial"),
        sa.CheckConstraint("type in ('water','electric')", name="ck_meter_type"),
    )

    op.create_table(
        "usage_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("meter_id", sa.Integer(), sa.ForeignKey("meters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tariff_id", sa.Integer(), sa.ForeignKey("tariffs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("consumption", sa.Float(), nullable=False),
        sa.Column("cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("meter_id", "period_start", "period_end", name="uq_meter_period"),
    )

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True),
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.Enum("pending", "paid", "overdue", "cancelled", name="invoice_status"), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("issued_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "period_start", "period_end", name="uq_invoice_period_per_tenant"),
    )

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("invoice_id", sa.Integer(), sa.ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.Enum("initiated", "succeeded", "failed", name="payment_status"), nullable=False),
        sa.Column("transaction_ref", sa.String(length=255), nullable=False),
        sa.Column("method", sa.String(length=50), nullable=True),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("transaction_ref", name="uq_transaction_ref"),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_audit_entity", "audit_logs", ["entity_type", "entity_id"])


def downgrade() -> None:
    op.drop_index("idx_audit_entity", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_table("payments")
    op.drop_table("invoices")
    op.drop_table("usage_records")
    op.drop_table("meters")
    op.drop_table("subscriptions")
    op.drop_table("tariffs")
    op.drop_table("tenants")
    op.drop_table("rooms")
    op.drop_table("floors")
    op.drop_table("buildings")
    op.drop_table("dorms")
