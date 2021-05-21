"""permissons for product package

Revision ID: f8f82c74f1fc
Revises: 1a46fdc4d630
Create Date: 2021-05-04 16:04:09.108771

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column, table

from auth_api.utils.custom_sql import CustomSql


# revision identifiers, used by Alembic.
revision = 'f8f82c74f1fc'
down_revision = '1a46fdc4d630'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    permissions_table = table('permissions',
                              column('id', sa.Integer()),
                              column('membership_type_code', sa.String(length=15)),
                              column('org_status_code', sa.String(length=25)),
                              column('actions', sa.String(length=100)))
    op.execute('delete from permissions where actions=\'request_product_package\'')
    conn = op.get_bind()
    res = conn.execute(
        f"select max(id) from permissions;")
    latest_id = res.fetchall()[0][0]

    # Insert code values
    op.bulk_insert(
        permissions_table,
        [
            {'id': latest_id + 1, 'membership_type_code': 'ADMIN', 'org_status_code': None,
             'actions': 'edit_request_product_package'},
            {'id': latest_id + 2, 'membership_type_code': 'COORDINATOR', 'org_status_code': None,
             'actions': 'edit_request_product_package'},
            {'id': latest_id + 3, 'membership_type_code': 'ADMIN', 'org_status_code': None,
             'actions': 'view_request_product_package'},
            {'id': latest_id + 4, 'membership_type_code': 'COORDINATOR', 'org_status_code': None,
             'actions': 'view_request_product_package'}
        ]
    )

    # ### end Alembic commands ###


def downgrade():
    op.execute('delete from permissions where actions in (\'edit_request_product_package\', \'view_request_product_package\')')
    # ### end Alembic commands ###
    permissions_table = table('permissions',
                              column('id', sa.Integer()),
                              column('membership_type_code', sa.String(length=15)),
                              column('org_status_code', sa.String(length=25)),
                              column('actions', sa.String(length=100)))

    conn = op.get_bind()
    res = conn.execute(
        f"select max(id) from permissions;")
    latest_id = res.fetchall()[0][0]

    # Insert code values
    op.bulk_insert(
        permissions_table,
        [
            {'id': latest_id + 1, 'membership_type_code': 'ADMIN', 'org_status_code': None,
             'actions': 'request_product_package'},
            {'id': latest_id + 2, 'membership_type_code': 'COORDINATOR', 'org_status_code': None,
             'actions': 'request_product_package'}
        ]
    )
