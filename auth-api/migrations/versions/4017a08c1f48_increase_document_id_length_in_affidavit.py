"""increase_document_id_length_in_affidavit

Revision ID: 4017a08c1f48
Revises: 648b36e69155
Create Date: 2020-06-16 11:45:48.440466

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '4017a08c1f48'
down_revision = '648b36e69155'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('affidavit', 'document_id',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.VARCHAR(length=60))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('affidavit', 'document_id',
                    existing_type=sa.VARCHAR(length=60),
                    type_=sa.VARCHAR(length=50))
    # ### end Alembic commands ###
