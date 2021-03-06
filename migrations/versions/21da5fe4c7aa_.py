"""empty message

Revision ID: 21da5fe4c7aa
Revises: 1c10b0d3b977
Create Date: 2021-08-16 20:58:22.767263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "21da5fe4c7aa"
down_revision = "1c10b0d3b977"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_first_name", table_name="users")
    op.drop_index("ix_users_last_name", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(length=60), autoincrement=False, nullable=True),
        sa.Column(
            "username", sa.VARCHAR(length=60), autoincrement=False, nullable=True
        ),
        sa.Column(
            "first_name", sa.VARCHAR(length=60), autoincrement=False, nullable=True
        ),
        sa.Column(
            "last_name", sa.VARCHAR(length=60), autoincrement=False, nullable=True
        ),
        sa.Column(
            "password", sa.VARCHAR(length=128), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=False)
    op.create_index("ix_users_last_name", "users", ["last_name"], unique=False)
    op.create_index("ix_users_first_name", "users", ["first_name"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    # ### end Alembic commands ###
