from sqlalchemy import create_engine, text

engine_meta = create_engine("mysql+pymysql://root:admin@localhost/meta")

with engine_meta.connect() as conn_meta:
    conn_meta.execute(text("INSERT INTO load_session (status) VALUES('not used')"))

    conn_meta.commit()
