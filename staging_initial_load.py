from transaction_data_prepare import retail_df, transacton_latest_file
from customer_data_prepare import customer_df, customer_latest_file
from staging_mapping import engine, transaction, customer, meta_load_history, transaction_load_history, customer_load_history
from sqlalchemy import insert, text,  update
from datetime import datetime


with engine.connect() as conn:


# TRANSACTION


# CUSTOMER
    meta_load_history_tbl = insert(meta_load_history).values(load_start_time=datetime.now(),
                                                                 load_end_time=None,
                                                                 load_status="In Progress",
                                                                 source=customer_latest_file
    )
    result = conn.execute(meta_load_history_tbl)
    current_load_session_id = result.inserted_primary_key[0]


# CUTOMER
    for _, row in customer_df.iterrows():

        customer_tbl_row = insert(customer).values(customer_id=row["Customer_ID"],
                                                   gender=row["Gender"],
                                                   date_of_birth=row["DOB"],
                                                   load_session_id = current_load_session_id
        )

        conn.execute(customer_tbl_row)


# CUSTOMER LOAD HISTORY
    for _, row in customer_df.iterrows():
        customer_hist_tbl_row = insert(customer_load_history).values(
                                                    load_session_id = current_load_session_id,
                                                    customer_id=row["Customer_ID"],
                                                    gender=row["Gender"],
                                                    date_of_birth=row["DOB"]


    )
        conn.execute(customer_hist_tbl_row)



    def get_imported_customer():
        count_customer = conn.execute(text("SELECT COUNT(customer_id) FROM customer"))
        count_res = count_customer.fetchone()
        res = count_res[0]
        return res


    imported_cust_numb = get_imported_customer()
    print(imported_cust_numb)

    customer_load_status = "Successful" if imported_cust_numb == len(customer_df) else "Failed"

    meta_load_history_tbl_update = (update(meta_load_history)
                                    .where(meta_load_history.c.load_session_id == current_load_session_id)
                                    .values(load_end_time=datetime.now(),
                                            load_status=customer_load_status)
                                    )

    conn.execute(meta_load_history_tbl_update)

    conn.commit()






