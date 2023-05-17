USE dw;

DELIMITER //

CREATE procedure load_dim_tbl()
BEGIN
	insert into dw.dim_invoice_date (date, year, quarter, month, week, day_name, created_datetime )
	select distinct
		 date(invoice_date)
		,year(invoice_date)
		,quarter(invoice_date)
		,month(invoice_date)
		,week(invoice_date)
		,dayname(invoice_date)
		,current_timestamp()
	from staging.transaction t
    where not exists (select invoice_date from dw.dim_invoice_date as d where invoice_date = date(t.invoice_date))
    ; 


	insert into dw.dim_customer (customer_id, gender, date_of_birth, country, created_datetime)
	select distinct
		c.customer_id
		,c.gender
		,c.date_of_birth
		,t.country
		,current_timestamp()
	from staging.customer as c join staging.transaction t on c.customer_id = t.customer_id
    where not exists (select customer_id from dw.dim_customer d where d.customer_id = c.customer_id)
    ;


	insert into dw.dim_product(stock_code, description, created_datetime)
	select distinct
		stock_code
		,description
		,current_timestamp()
	from staging.transaction t
    where not exists (select stock_code from dw.dim_product d where d.stock_code = t.stock_code)
    ; 


	insert into dw.dim_invoice(invoice_id, customer_key, valid, created_datetime)
	select 
		 vt.invoice_id
		,1
		,current_timestamp()
	from dw.valid_transaction_view as vt
    where not exists (select invoice_id from dw.dim_invoice d where d.invoice_id = vt.invoice_id)
	UNION
	select 
		 ct.invoice_id
		,0
		,current_timestamp()
	from dw.cancelled_transaction_view as ct
    where not exists (select invoice_id from dw.dim_invoice d where d.invoice_id = ct.invoice_id)
    ;

END //

DELIMITER ;