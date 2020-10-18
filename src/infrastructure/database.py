import os

from sqlalchemy import (
    Column,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
)

metadata = MetaData()

reports_table = Table(
    'report', metadata,
    Column('patient_id', String(250), primary_key=True),
    Column('document_text', Text, nullable=False)
)


def init_db_engine(db_uri=None):
    uri = db_uri or os.getenv('DB_URI')
    db_engine = create_engine(uri, convert_unicode=True)
    __create_tables_if_not_exists(db_engine)
    return db_engine


def db_connect(db_engine):
    return db_engine.connect()


def close_db_connection(db_connection):
    try:
        db_connection.close()
    except:
        pass


def __create_tables_if_not_exists(db_engine):
    # NOTE:  use Alembic for migrations (https://alembic.sqlalchemy.org/en/latest/)
    reports_table.create(db_engine, checkfirst=True)
