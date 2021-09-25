"""ADD theia session k8s requested boolean

Revision ID: c8cb0e5a0950
Revises: 3150c9c06ea5
Create Date: 2021-09-25 18:05:03.669828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "c8cb0e5a0950"
down_revision = "3150c9c06ea5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "theia_session",
        sa.Column("k8s_requested", sa.Boolean(), nullable=True),
    )
    op.drop_column("theia_session", "last_heartbeat")

    conn = op.get_bind()
    with conn.begin():
        conn.execute("update theia_session set k8s_requested = 1;")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "theia_session",
        sa.Column("last_heartbeat", mysql.DATETIME(), nullable=True),
    )
    op.drop_column("theia_session", "k8s_requested")
    # ### end Alembic commands ###
