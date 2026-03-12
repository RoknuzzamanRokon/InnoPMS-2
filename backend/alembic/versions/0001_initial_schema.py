"""Initial starter PMS schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-03-10 00:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "property",
        sa.Column("property_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("property_type", sa.String(length=100), nullable=False),
        sa.Column("star_rating", sa.SmallInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "rate_plan",
        sa.Column("rate_plan_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("property_id", sa.BigInteger(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("base_rate", sa.Numeric(10, 2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("apply_to", sa.Enum("per_room", "per_person", "per_stay", name="apply_to_enum"), nullable=False),
        sa.ForeignKeyConstraint(["property_id"], ["property.property_id"], ondelete="CASCADE"),
    )

    op.create_table(
        "room",
        sa.Column("room_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("property_id", sa.BigInteger(), nullable=False),
        sa.Column("building_id", sa.BigInteger(), nullable=True),
        sa.Column("room_type_id", sa.BigInteger(), nullable=False),
        sa.Column("room_number", sa.String(length=50), nullable=False),
        sa.Column("floor", sa.String(length=50), nullable=True),
        sa.Column("room_status", sa.Enum("vacant", "occupied", "out_of_order", name="room_status_enum"), nullable=False),
        sa.ForeignKeyConstraint(["property_id"], ["property.property_id"], ondelete="CASCADE"),
        sa.UniqueConstraint("property_id", "room_number", name="uq_room_property_room_number"),
    )

    op.create_table(
        "room_inventory",
        sa.Column("inventory_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("property_id", sa.BigInteger(), nullable=False),
        sa.Column("room_type_id", sa.BigInteger(), nullable=False),
        sa.Column("inventory_date", sa.Date(), nullable=False),
        sa.Column("total_rooms", sa.SmallInteger(), nullable=False),
        sa.Column("available_rooms", sa.SmallInteger(), nullable=False),
        sa.Column("booked_rooms", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("blocked_rooms", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["property_id"], ["property.property_id"], ondelete="CASCADE"),
        sa.UniqueConstraint(
            "property_id",
            "room_type_id",
            "inventory_date",
            name="uq_room_inventory_property_room_type_date",
        ),
    )


def downgrade() -> None:
    op.drop_table("room_inventory")
    op.drop_table("room")
    op.drop_table("rate_plan")
    op.drop_table("property")
