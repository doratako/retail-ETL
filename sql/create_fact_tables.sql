use dw;

create table fact_valid_transaction
(
invoice_date_key int not null,
invoice_key int not null,
customer_key int not null,
product_key int not null,
quantity int not null,
unit_price float not null,
created_datetime timestamp not null,
FOREIGN KEY(invoice_date_key) references dim_invoice_date(invoice_date_key),
FOREIGN KEY(invoice_key) references dim_invoice(invoice_key),
FOREIGN KEY(customer_key) references dim_customer(customer_key),
FOREIGN KEY(product_key) references dim_product(product_key)
);


create table fact_cancelled_transaction
(
invoice_date_key int not null,
invoice_key int not null,
customer_key int not null,
product_key int not null,
quantity int not null,
unit_price float not null,
created_datetime timestamp not null,
FOREIGN KEY(invoice_date_key) references dim_invoice_date(invoice_date_key),
FOREIGN KEY(invoice_key) references dim_invoice(invoice_key),
FOREIGN KEY(customer_key) references dim_customer(customer_key),
FOREIGN KEY(product_key) references dim_product(product_key)
);


create table fact_daily_sales
(
invoice_date_key int not null,
daily_revenue float not null,
daily_total_unit_sold int not null,
daily_avg_unit_price float not null,
created_datetime timestamp not null,
FOREIGN KEY(invoice_date_key) references dim_invoice_date(invoice_date_key)
);


create table fact_monthly_product_sales
(
invoice_year int not null,
invoice_month int not null,
product_key int not null,
monthly_unit_sold integer not null,
monthly_revenue float not null,
num_customers integer not null,
created_datetime timestamp not null,
FOREIGN KEY(product_key) references dim_product(product_key)
);



create table fact_daily_customer_sales
(
invoice_date_key int not null,
customer_key int not null,
num_invoices int not null,
units_bought_per_customer int not null,
customer_total_spend float not null,
created_datetime timestamp not null,
FOREIGN KEY(invoice_date_key) references dim_invoice_date(invoice_date_key),
FOREIGN KEY(customer_key) references dim_customer(customer_key)
);
