-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS coffee_shop;
USE coffee_shop;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role ENUM('admin', 'staff') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_time DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

-- Insert default admin user if not exists
INSERT IGNORE INTO users (username, password, email, role) VALUES ('admin', 'admin123', 'trandat262075@gmail.com', 'admin');
INSERT IGNORE INTO users (username, password, email, role) VALUES ('staff', 'staff123', 'staff@coffee.com', 'staff');

-- Insert sample menu items
INSERT IGNORE INTO menu_items (name, description, price, category) VALUES
('Espresso', 'Strong brewed coffee', 2.50, 'Hot Coffee'),
('Cappuccino', 'Espresso with steamed milk foam', 3.50, 'Hot Coffee'),
('Latte', 'Espresso with steamed milk', 3.50, 'Hot Coffee'),
('Americano', 'Espresso with hot water', 3.00, 'Hot Coffee'),
('Iced Coffee', 'Cold brewed coffee with ice', 3.00, 'Cold Coffee'),
('Iced Latte', 'Espresso with cold milk and ice', 4.00, 'Cold Coffee'),
('Green Tea', 'Japanese green tea', 2.50, 'Tea'),
('Earl Grey', 'Black tea with bergamot', 2.50, 'Tea'),
('Chocolate Cake', 'Rich chocolate layer cake', 4.50, 'Dessert'),
('Croissant', 'Butter croissant', 2.50, 'Pastry'),
('Muffin', 'Blueberry muffin', 2.00, 'Pastry');

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_menu_items_category ON menu_items(category);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- Add UNIQUE constraint to menu_items name if not exists
ALTER TABLE menu_items ADD UNIQUE INDEX IF NOT EXISTS idx_menu_items_name (name);