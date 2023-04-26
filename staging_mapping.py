from sqlalchemy import Table, Column, Integer, Float, String, DateTime, Date, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

engine = create_engine("mysql+pymysql://root:admin@localhost/staging")

meta = MetaData()

# STAGING TABLES
transaction = Table(
    "transaction",
    meta,
    Column("invoice_id", String(20),  nullable=False),
    Column("stock_code", String(20)),
    Column("description", String(100)),
    Column("quantity", Integer),
    Column("invoice_date", DateTime),
    Column("unit_price", Float),
    Column("customer_id", Integer, nullable=False),
    Column("country", String(80)),
    Column("load_session_id", Integer, nullable=False),
)

customer = Table(
    "customer",
    meta,
    Column("customer_id", Integer, nullable=False),
    Column("gender", String(20)),
    Column("date_of_birth", Date),
    Column("load_session_id", Integer,  nullable=False)
)

meta_load_history = Table(
    "meta_load_history",
    meta,
    Column("load_session_id", Integer, nullable=False),
    Column("load_start_time", DateTime),
    Column("load_end_time", DateTime),
    Column("load_status", String(20)),
    Column("source", String(100))
)


transaction_load_history = Table(
    "transaction_load_history",
    meta,
    Column("load_session_id", Integer, nullable=False),
    Column("invoice_id", String(20), nullable=False),
    Column("stock_code", String(20)),
    Column("description", String(100)),
    Column("quantity", Integer),
    Column("invoice_date", DateTime),
    Column("unit_price", Float),
    Column("customer_id", Integer, nullable=False),
    Column("country", String(80)),
)


customer_load_history = Table(
    "customer_load_history",
    meta,
    Column("load_session_id", Integer, nullable=False),
    Column("customer_id", Integer, nullable=False),
    Column("gender", String(20)),
    Column("date_of_birth", Date),
)

try:
    meta.create_all(engine)
except OperationalError as error:
    print(f"Error connecting to the database: {error}")



