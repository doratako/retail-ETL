USE dw;

DELIMITER //
CREATE procedure load_dw_view()
BEGIN
	CREATE OR REPLACE VIEW dw.cancelled_transaction_view AS
    SELECT 
        staging.transaction.invoice_id AS invoice_id,
        staging.transaction.stock_code AS stock_code,
        staging.transaction.description AS description,
        staging.transaction.quantity AS quantity,
        staging.transaction.invoice_date AS invoice_date,
        staging.transaction.unit_price AS unit_price,
        staging.transaction.customer_id AS customer_id, 
        current_timestamp() AS created_datetime
    FROM
        staging.transaction
    WHERE
        staging.transaction.quantity < 0
        ;
        
        
	CREATE OR REPLACE VIEW dw.valid_transaction_view AS
    SELECT 
        staging.transaction.invoice_id AS invoice_id,
        staging.transaction.stock_code AS stock_code,
        staging.transaction.description AS description,
        staging.transaction.quantity AS quantity,
        staging.transaction.invoice_date AS invoice_date,
        staging.transaction.unit_price AS unit_price,
        staging.transaction.customer_id AS customer_id,
        current_timestamp() AS created_datetime
    FROM
        staging.transaction
    WHERE
        staging.transaction.quantity > 0
        ;   
        
	
        
END//
DELIMITER ;
