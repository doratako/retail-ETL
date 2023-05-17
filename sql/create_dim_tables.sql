use dw;

create table dim_invoice_date
( 
 invoice_date_key int auto_increment not null,
 date date not null, 
 year int not null,
 quarter int not null, 
 month int not null,
 week int not null,
 day_name varchar(10) not null,
 created_datetime timestamp not null,
PRIMARY KEY(invoice_date_key)
);


create table dim_customer
(
 customer_key int auto_increment not null,
 customer_id int not null,
 gender varchar(10) not null,
 date_of_birth date not null,
 country varchar(80) not null,
 created_datetime timestamp not null,  
 PRIMARY KEY(customer_key),
 );
 
 
 create table dim_product
 (
 product_key int auto_increment not null,
 stock_code varchar(20) not null,
 description varchar(100) not null,
 created_datetime timestamp not null,
 PRIMARY KEY(product_key)
 );
 

create table dim_invoice
( 
 invoice_key int auto_increment not null,
 invoice_id varchar(20) not null,
 valid varchar(1) not null,
 created_datetime timestamp not null,
PRIMARY KEY(invoice_key),
FOREIGN KEY(customer_key) references dim_customer(customer_key)
);




