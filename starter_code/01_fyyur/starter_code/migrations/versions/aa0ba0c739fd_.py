"""empty message

Revision ID: aa0ba0c739fd
Revises: 
Create Date: 2020-03-04 14:58:02.423310

"""
import os
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy_searchable import sync_trigger
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


# revision identifiers, used by Alembic.
revision = 'aa0ba0c739fd'
down_revision = None
branch_labels = None
depends_on = None

def run_sqlalchemy_searchable_sql():
    """
    With alembic and sqlalchemy_searchable we run SQL statements before table creation. These statements enable searching
    See:
    - https://conorliv.com/alembic-migration-execute-raw-sql.html
    - https://github.com/kvesteri/sqlalchemy-searchable/issues/67
    """
    sql_expressions = Path('alembic').joinpath('searchable_expressions.sql').open().read()
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(sql_expressions)

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    op.create_table('Artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
    sync_trigger(conn,'Venue','search_vector',['name']),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute()
    op.create_index('ix_Venue_search_vector', 'Venue', ['search_vector'], unique=False, postgresql_using='gin'),

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    op.drop_table('Venue')
    op.drop_table('Artist')
    op.drop_index('ix_Venue_search_vector', table_name='Venue')
    sync_trigger(conn,'Venue','search_vector',['name'])
    # ### end Alembic commands ###