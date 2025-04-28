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
(1, 101, '2025-01-01', 100.00),
(2, 102, '2025-01-02', 150.50),
(3, 103, '2025-01-03', 200.75),
(4, 104, '2025-01-04', 250.00),
(5, 105, '2025-01-05', 300.25);