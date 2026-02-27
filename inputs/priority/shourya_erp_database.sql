-- Shourya Bharatgas ERP Database Schema
-- Run this in phpMyAdmin to create the database

CREATE DATABASE IF NOT EXISTS shourya_erp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shourya_erp;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role ENUM('owner','manager','delivery','bda','temp') NOT NULL,
    designation VARCHAR(100),
    mobile VARCHAR(15),
    alt_mobile VARCHAR(15),
    area VARCHAR(100),
    salary VARCHAR(50),
    eo_id VARCHAR(50),
    active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Deliveries table
CREATE TABLE deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sl_no INT,
    area VARCHAR(100),
    consumer_number VARCHAR(50),
    consumer_name VARCHAR(200),
    address TEXT,
    mobile VARCHAR(15),
    cash_memo VARCHAR(50),
    operator_id VARCHAR(50),
    operator_name VARCHAR(100),
    book_date DATE,
    cash_memo_date DATE,
    status ENUM('scheduled','intrip','delivered','emergency','notdelivered') DEFAULT 'scheduled',
    otp VARCHAR(10),
    payment_mode VARCHAR(50),
    amount DECIMAL(10,2) DEFAULT 856.00,
    delivered_by INT,
    delivered_at TIMESTAMP NULL,
    notes TEXT,
    gps_lat DECIMAL(10,8),
    gps_lng DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_operator (operator_name),
    INDEX idx_area (area),
    FOREIGN KEY (delivered_by) REFERENCES users(id)
);

-- Godown stock table
CREATE TABLE godown_stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    cylinder_type ENUM('14.2_full','14.2_empty','5_full','5_empty','19_full','19_empty') NOT NULL,
    opening INT DEFAULT 0,
    received INT DEFAULT 0,
    delivered INT DEFAULT 0,
    closing INT DEFAULT 0,
    defective INT DEFAULT 0,
    bda_stock INT DEFAULT 0,
    vehicle_stock INT DEFAULT 0,
    notes TEXT,
    recorded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_date_type (date, cylinder_type),
    FOREIGN KEY (recorded_by) REFERENCES users(id)
);

-- Office stock (accessories)
CREATE TABLE office_accessories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    opening INT DEFAULT 0,
    received INT DEFAULT 0,
    sold INT DEFAULT 0,
    closing INT DEFAULT 0,
    last_updated DATE,
    updated_by INT,
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Trips table
CREATE TABLE trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_date DATE NOT NULL,
    delivery_man INT NOT NULL,
    status ENUM('planned','active','completed') DEFAULT 'planned',
    full_14_given INT DEFAULT 0,
    empty_14_taken INT DEFAULT 0,
    full_5_given INT DEFAULT 0,
    empty_5_taken INT DEFAULT 0,
    cash_collected DECIMAL(10,2) DEFAULT 0,
    online_collected DECIMAL(10,2) DEFAULT 0,
    total_deliveries INT DEFAULT 0,
    notes TEXT,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (delivery_man) REFERENCES users(id)
);

-- Cash transactions
CREATE TABLE cash_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trans_date DATE NOT NULL,
    trans_type ENUM('opening','collection','expense','transfer','closing') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    from_user INT,
    to_user INT,
    recorded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_user) REFERENCES users(id),
    FOREIGN KEY (to_user) REFERENCES users(id),
    FOREIGN KEY (recorded_by) REFERENCES users(id)
);

-- Payroll table
CREATE TABLE payroll (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    month_year VARCHAR(10) NOT NULL,
    urban_cylinders INT DEFAULT 0,
    rural_cylinders INT DEFAULT 0,
    pair_days INT DEFAULT 0,
    gross_wages DECIMAL(10,2) DEFAULT 0,
    cash_difference DECIMAL(10,2) DEFAULT 0,
    advance_deduction DECIMAL(10,2) DEFAULT 0,
    net_wages DECIMAL(10,2) DEFAULT 0,
    advance_balance DECIMAL(10,2) DEFAULT 0,
    status ENUM('draft','submitted','approved','paid') DEFAULT 'draft',
    approved_by INT,
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_month (user_id, month_year),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- BDA areas table
CREATE TABLE bda_areas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    area_name VARCHAR(100) NOT NULL,
    owner_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15),
    user_id INT,
    active TINYINT(1) DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- System settings
CREATE TABLE settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Notices
CREATE TABLE notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    priority ENUM('urgent','notice','info') DEFAULT 'info',
    posted_by INT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

-- Insert default users
INSERT INTO users (username, password, name, role, designation, mobile, alt_mobile, salary, eo_id) VALUES
('owner', '$2y$10$YourHashedPasswordHere', 'Vishal Patil', 'owner', 'Owner & Partner', '7887456789', '9869234868', 'na', NULL),
('owner2', '$2y$10$YourHashedPasswordHere', 'Mrinmayi Patil', 'owner', 'Owner & Partner', '8080802880', '', 'na', NULL),
('manager', '$2y$10$YourHashedPasswordHere', 'Rajesh Awale', 'manager', 'Manager', '8007183197', '', '15000', NULL),
('delivery_bhore', '$2y$10$YourHashedPasswordHere', 'Vishwas Bhore', 'delivery', 'Delivery Man', '7643982982', '9975464383', 'urban+rural', 'EO18761810000007'),
('delivery_mahesh', '$2y$10$YourHashedPasswordHere', 'Mahesh Patil', 'delivery', 'Delivery Man', '8830669611', '', 'urban+rural', 'EO18761810000010'),
('delivery_harun', '$2y$10$YourHashedPasswordHere', 'Harun Fakir', 'delivery', 'Delivery Man', '9970660901', '', 'urban+rural', 'EO18761810000006'),
('delivery_magdum', '$2y$10$YourHashedPasswordHere', 'Vishal Magdum', 'delivery', 'Delivery Man', '9096853954', '7643987987', 'urban+rural', NULL);

-- Insert BDA areas
INSERT INTO bda_areas (area_name, owner_name, mobile) VALUES
('Kondigre', 'Sarika Waghmode', '9561242972'),
('Nimshirgav', 'Kumar Thomake', '9673824646'),
('Nimshirgav', 'Lakhane', '7588262265'),
('Danoli', 'Manoj', '9970731436'),
('Kothali', 'Yadav', '9405744020'),
('Kavatesar', 'Sudhakar Patil', '9822180498'),
('Shirol', 'Vikrant Kamble', '7028502299'),
('Chipri Beghar', 'Rajesh Awale', '8007183197');

-- Insert default settings
INSERT INTO settings (setting_key, setting_value) VALUES
('cylinder_14_price', '856'),
('cylinder_5_price', '420'),
('cylinder_19_price', '1923'),
('urban_wage', '8'),
('rural_wage', '7'),
('pair_bonus', '200'),
('company_name', 'Shourya Bharatgas Services'),
('sap_code', '187618'),
('gstin', '');

-- Insert initial accessories
INSERT INTO office_accessories (item_name, opening, received, sold, closing) VALUES
('Blue Book', 100, 0, 0, 100),
('Suraksha Pipe', 50, 0, 0, 50),
('DPR 14.2', 338, 0, 0, 338),
('DPR 5kg', 62, 0, 0, 62);
