"""USER: changed dob and expiry fields to Date

Revision ID: 6fe7af4ed2f0
Revises: 72eb109dc914
Create Date: 2023-09-21 18:34:06.547410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fe7af4ed2f0'
down_revision = '72eb109dc914'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('dob',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)
        batch_op.alter_column('expiry_date',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('expiry_date',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)
        batch_op.alter_column('dob',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
