USE dw;

DELIMITER //
CREATE procedure load_fact_tbl()
BEGIN
	insert into dw.fact_valid_transaction (invoice_date_key, invoice_key, customer_key, product_key, quantity, unit_price, created_datetime)
	select 
		id.invoice_date_key
	   ,i.invoice_key
	   ,c.customer_key
	   ,p.product_key
	   ,vt.quantity
	   ,vt.unit_price
	   ,current_timestamp()
	from dw.valid_transaction_view as vt 
		join dw.dim_invoice_date as id on date(vt.invoice_date) = id.date
		join dw.dim_invoice as i  on vt.invoice_id = i.invoice_id
		join dw.dim_customer as c on vt.customer_id = c.customer_id
		join dw.dim_product as p on vt.stock_code = p.stock_code and vt.description = p.description
		;
 

	 insert into dw.fact_cancelled_transaction (invoice_date_key, invoice_key, customer_key, product_key, quantity, unit_price, created_datetime)
	select 
		id.invoice_date_key
	   ,i.invoice_key
	   ,c.customer_key
	   ,p.product_key
	   ,vt.quantity
	   ,vt.unit_price
	   ,current_timestamp()
	from dw.cancelled_transaction_view as vt 
		join dw.dim_invoice_date as id on date(vt.invoice_date) = id.date
		join dw.dim_invoice as i  on vt.invoice_id = i.invoice_id
		join dw.dim_customer as c on vt.customer_id = c.customer_id
		join dw.dim_product as p on vt.stock_code = p.stock_code and vt.description = p.description
        ;


	insert into dw.fact_daily_sales (invoice_date_key, daily_revenue, daily_total_unit_sold, daily_avg_unit_price, created_datetime )
	select 
		id.invoice_date_key
		,round(sum(vt.quantity * vt.unit_price), 2) as daily_revenue
		,count(p.stock_code) as daily_total_unit_sold
		,round(avg(vt.unit_price),2) as daily_avg_unit_price
		,current_timestamp()
	from dw.valid_transaction_view as vt 
		join dw.dim_invoice_date as id on date(vt.invoice_date) = id.date
		join dw.dim_product as p on vt.stock_code = p.stock_code and vt.description = p.description
	group by id.date, id.invoice_date_key
	;



	insert into dw.fact_monthly_product_sales
	(
	select  
		 id.year as invoice_year
		,id.month as invoice_month
		,p.product_key as product_key
		, sum(vt.quantity) as monthly_unit_sold
		,round(sum(vt.quantity * vt.unit_price), 2) as monthly_revenue
		,count(distinct c.customer_id) as num_customers
		,current_timestamp()
	from dw.valid_transaction_view as vt
		join dw.dim_invoice_date as id on date(vt.invoice_date) = id.date
		join dw.dim_product as p on vt.stock_code = p.stock_code and vt.description = p.description
		join dw.dim_customer as c on vt.customer_id = c.customer_id
	group by id.year, id.month, p.product_key
	order by id.year, id.month, p.product_key
	);


	insert into dw.fact_daily_customer_sales
	(
	select 
		id.invoice_date_key
		,c.customer_key
		,count(distinct invoice_id) as num_invoices
		,count(stock_code) as units_bought_per_customer
		,round(sum(unit_price*quantity), 2) as customer_total_spend
		,current_timestamp()
	from dw.valid_transaction_view as vt
		join dw.dim_invoice_date as id on date(vt.invoice_date) = id.date
		join dw.dim_customer as c on vt.customer_id = c.customer_id
	group by id.invoice_date_key, c.customer_key 
	);
		

END //
DELIMITER ;