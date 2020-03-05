"""empty message

Revision ID: ea97bcde1b14
Revises: 59383b159fe5
Create Date: 2020-02-28 15:35:48.400247

"""
import os
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy_searchable import sync_trigger
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


# revision identifiers, used by Alembic.
revision = 'ea97bcde1b14'
down_revision = '59383b159fe5'
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
    conn = op.get_bind()
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True))
    op.create_index('ix_Venue_search_vector', 'Venue', ['search_vector'], unique=False, postgresql_using='gin')
    sync_trigger(conn,'Venue','search_vector',['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    op.drop_index('ix_Venue_search_vector', table_name='Venue')
    op.drop_column('Venue', 'search_vector')
    sync_trigger(conn,'Venue','search_vector',['name'])
    # ### end Alembic commands ###
