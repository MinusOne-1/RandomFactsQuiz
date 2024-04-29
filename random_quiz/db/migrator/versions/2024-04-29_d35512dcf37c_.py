"""empty message

Revision ID: d35512dcf37c
Revises: 
Create Date: 2024-04-29 22:38:09.440436

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'd35512dcf37c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "dt_created",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "dt_updated",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("username", sa.TEXT(), nullable=False),
        sa.Column("password", sa.TEXT(), nullable=False),
        sa.Column("email", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user")),
        sa.UniqueConstraint("id", name=op.f("uq__user__id")),
    )
    op.create_index(op.f("ix__user__password"), "user", ["password"], unique=False)
    op.create_index(op.f("ix__user__username"), "user", ["username"], unique=True)
    op.create_unique_constraint(op.f("uq__user__id"), "user", ["id"])

def downgrade():

    op.drop_constraint(op.f("uq__user__id"), "user", type_="unique")
    op.drop_index(op.f("ix__user__username"), table_name="user")
    op.drop_index(op.f("ix__user__password"), table_name="user")
    op.drop_table("user")

