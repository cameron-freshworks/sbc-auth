"""add_user_status

Revision ID: 70d2fe46051f
Revises: dede70a6df1e
Create Date: 2019-11-28 13:18:02.714206

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '70d2fe46051f'
down_revision = 'dede70a6df1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    user_status_code = op.create_table('user_status_code',
                                sa.Column('created', sa.DateTime(), nullable=True),
                                sa.Column('modified', sa.DateTime(), nullable=True),
                                sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                                sa.Column('name', sa.String(length=15), nullable=True),
                                sa.Column('description', sa.String(length=100), nullable=True),
                                sa.Column('created_by_id', sa.Integer(), nullable=True),
                                sa.Column('modified_by_id', sa.Integer(), nullable=True),
                                sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
                                sa.ForeignKeyConstraint(['modified_by_id'], ['user.id'], ),
                                sa.PrimaryKeyConstraint('id')
                                )
    op.add_column('user', sa.Column('status', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'user_status_code', ['status'], ['id'])
    
    # Insert code values
    op.bulk_insert(
        user_status_code,
        [
            {'id': '1', 'name': 'ACTIVE', 'description': 'Active Users ;Active in the system'},
            {'id': '2', 'name': 'INACTIVE', 'description': 'Inactive Users;Not fetched anywhere'}
        ]
    )

    # Update all existing user records to active
    op.execute('update "user" set status=(select id from user_status_code where name=\'ACTIVE\')')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'status')
    op.drop_table('user_status_code')
    # ### end Alembic commands ###
