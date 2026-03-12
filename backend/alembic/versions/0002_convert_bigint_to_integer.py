"""Convert BIGINT identifiers to INTEGER.

Revision ID: 0002_convert_bigint_to_integer
Revises: 0001_initial_schema
Create Date: 2026-03-12 12:50:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0002_convert_bigint_to_integer"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def _drop_fk_if_exists(table_name: str, constrained_columns: list[str]) -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for fk in inspector.get_foreign_keys(table_name):
        if fk.get("constrained_columns") == constrained_columns and fk.get("name"):
            op.drop_constraint(fk["name"], table_name, type_="foreignkey")
            break


def upgrade() -> None:
    _drop_fk_if_exists("rate_plan", ["property_id"])
    _drop_fk_if_exists("room", ["property_id"])
    _drop_fk_if_exists("room_inventory", ["property_id"])

    op.alter_column(
        "property",
        "property_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )

    op.alter_column(
        "rate_plan",
        "rate_plan_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "rate_plan",
        "property_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
    )

    op.alter_column(
        "room",
        "room_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "room",
        "property_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "room",
        "building_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=True,
    )
    op.alter_column(
        "room",
        "room_type_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
    )

    op.alter_column(
        "room_inventory",
        "inventory_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "room_inventory",
        "property_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.alter_column(
        "room_inventory",
        "room_type_id",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
    )

    op.create_foreign_key(None, "rate_plan", "property", ["property_id"], ["property_id"], ondelete="CASCADE")
    op.create_foreign_key(None, "room", "property", ["property_id"], ["property_id"], ondelete="CASCADE")
    op.create_foreign_key(None, "room_inventory", "property", ["property_id"], ["property_id"], ondelete="CASCADE")


def downgrade() -> None:
    _drop_fk_if_exists("rate_plan", ["property_id"])
    _drop_fk_if_exists("room", ["property_id"])
    _drop_fk_if_exists("room_inventory", ["property_id"])

    op.alter_column(
        "property",
        "property_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        autoincrement=True,
    )

    op.alter_column(
        "rate_plan",
        "rate_plan_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "rate_plan",
        "property_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )

    op.alter_column(
        "room",
        "room_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "room",
        "property_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.alter_column(
        "room",
        "building_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=True,
    )
    op.alter_column(
        "room",
        "room_type_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )

    op.alter_column(
        "room_inventory",
        "inventory_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        autoincrement=True,
    )
    op.alter_column(
        "room_inventory",
        "property_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.alter_column(
        "room_inventory",
        "room_type_id",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )

    op.create_foreign_key(None, "rate_plan", "property", ["property_id"], ["property_id"], ondelete="CASCADE")
    op.create_foreign_key(None, "room", "property", ["property_id"], ["property_id"], ondelete="CASCADE")
    op.create_foreign_key(None, "room_inventory", "property", ["property_id"], ["property_id"], ondelete="CASCADE")
