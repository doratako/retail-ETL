from transaction_data_prepare import retail_df, transaction_latest_file
from customer_data_prepare import customer_df, customer_latest_file
from staging_mapping import engine, transaction, customer, meta_load_history, transaction_load_history, customer_load_history
from meta_db import engine_meta
from sqlalchemy import insert, text,  update
from datetime import datetime

# getting the latest load_session_id from meta schema
with engine_meta.connect() as conn_meta:
    initial_load_session_id = conn_meta.execute(text("SELECT max(load_session_id) FROM load_session")).fetchone()[0]
    conn_meta.execute(text(f"UPDATE load_session SET status='closed' WHERE load_session_id={initial_load_session_id}"))

    conn_meta.commit()

# STAGE database
with engine.connect() as conn:

# META_LOAD_HISTORY
    source_files = [transaction_latest_file, customer_latest_file]

    for file in source_files:
        meta_load_history_tbl = insert(meta_load_history).values(load_session_id=initial_load_session_id,
                                                                     load_start_time=datetime.now(),
                                                                     load_end_time=None,
                                                                     load_status="In Progress",
                                                                     source=file
        )

        conn.execute(meta_load_history_tbl)


# TRANSACTION
    for _, row in retail_df.iterrows():
        transaction_tbl_row = insert(transaction).values(invoice_id=row["Invoice_ID"],
                                                          stock_code=row["StockCode"],
                                                          description=row["Description"],
                                                          quantity=row["Quantity"],
                                                          invoice_date=row["InvoiceDate"],
                                                          unit_price=row["UnitPrice"],
                                                          customer_id=row["Customer_ID"],
                                                          country=row["Country"],
                                                          load_session_id=initial_load_session_id
                                                          )
        conn.execute(transaction_tbl_row)


# TRANSACTION_LOAD_HISTORY
    for _, row in retail_df.iterrows():
        transaction_tbl_row = insert(transaction).values(invoice_id=row["Invoice_ID"],
                                                          stock_code=row["StockCode"],
                                                          description=row["Description"],
                                                          quantity=row["Quantity"],
                                                          invoice_date=row["InvoiceDate"],
                                                          unit_price=row["UnitPrice"],
                                                          customer_id=row["Customer_ID"],
                                                          country=row["Country"],
                                                          load_session_id = initial_load_session_id
                                                          )
        conn.execute(transaction_tbl_row)


# CUSTOMER
    for _, row in customer_df.iterrows():

        customer_tbl_row = insert(customer).values(customer_id=row["Customer_ID"],
                                                   gender=row["Gender"],
                                                   date_of_birth=row["DOB"],
                                                   load_session_id = initial_load_session_id
        )

        conn.execute(customer_tbl_row)


# CUSTOMER_LOAD_HISTORY
    for _, row in customer_df.iterrows():
        customer_hist_tbl_row = insert(customer_load_history).values(
                                                    load_session_id = initial_load_session_id,
                                                    customer_id=row["Customer_ID"],
                                                    gender=row["Gender"],
                                                    date_of_birth=row["DOB"]
    )
        conn.execute(customer_hist_tbl_row)


    # comparing the number of rows in source files and db tables to evaluate the status of the load session
    def get_num_imported_rows():
        count_transaction = conn.execute(text("SELECT COUNT(load_session_id) FROM transaction")).fetchone()[0]
        count_customer = conn.execute(text("SELECT COUNT(load_session_id) FROM customer")).fetchone()[0]

        return count_transaction, count_customer

    num_rows = get_num_imported_rows()
    (transaction_imported_rows, customer_imported_rows) = num_rows

    transaction_load_status = "Successful" if transaction_imported_rows == len(retail_df) else "Failed"
    customer_load_status = "Successful" if customer_imported_rows == len(customer_df) else "Failed"

    status = [transaction_load_status, customer_load_status]

    for i in range(len(source_files)):
        meta_load_history_tbl_update = (update(meta_load_history)
                                        .where(meta_load_history.c.load_session_id == initial_load_session_id)
                                        .values(load_end_time=datetime.now(),
                                                load_status=status[i])
                                        )
        conn.execute(meta_load_history_tbl_update)

    conn.commit()






