"""ADD github_repo_required to assignment

Revision ID: ba7750bc4d14
Revises: 2f5a27ffe4ea
Create Date: 2021-08-09 12:26:42.507719

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "ba7750bc4d14"
down_revision = "2f5a27ffe4ea"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "assignment",
        sa.Column("github_repo_required", sa.Boolean(), nullable=True),
    )
    conn = op.get_bind()
    with conn.begin():
        conn.execute("update assignment set github_repo_required = 1;")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("assignment", "github_repo_required")
    # ### end Alembic commands ###
