from sqlalchemy import text
from staging_mapping import engine
from staging_initial_load import get_unique_session_id, load_stage_tables


with engine.connect() as conn:

    conn.execute(text("TRUNCATE customer"))
    conn.execute(text("TRUNCATE transaction"))

    get_unique_session_id()
    load_stage_tables()


