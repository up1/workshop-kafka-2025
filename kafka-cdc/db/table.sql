use inventory;
-- Create table orders
CREATE TABLE inventory.orders (
    order_number INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2)
);

-- Insert sample data into orders
INSERT INTO inventory.orders (order_number, customer_id, order_date, total_amount) VALUES
(1, 101, now(), 100.00),
(2, 102, now(), 150.50),
(3, 103, now(), 200.75),
(4, 104, now(), 250.00),
(5, 105, now(), 300.25);