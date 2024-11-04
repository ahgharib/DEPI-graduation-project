-- Create Data Warehouse Database
CREATE DATABASE FeedbackWarehouse;
GO

-- Use the new warehouse database
USE FeedbackWarehouse;
GO

-- Create DimCustomer
CREATE TABLE DimCustomer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(255),
    state VARCHAR(100)
);

-- Create DimStore
CREATE TABLE DimStore (
    store_id INT PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    address VARCHAR(255)
);

-- Create DimProduct
CREATE TABLE DimProduct (
    product_id INT PRIMARY KEY,
    name VARCHAR(255),
    price FLOAT
);

-- Create DimDate
CREATE TABLE DimDate (
    date_id INT IDENTITY(1,1) PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    day INT
);

-- Create FactFeedback
CREATE TABLE FactFeedback (
    feedback_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT,
    store_id INT,
    product_id INT,
    date_id INT,
    review TEXT,
    rating INT,
    FOREIGN KEY (customer_id) REFERENCES DimCustomer(customer_id),
    FOREIGN KEY (store_id) REFERENCES DimStore(store_id),
    FOREIGN KEY (product_id) REFERENCES DimProduct(product_id),
    FOREIGN KEY (date_id) REFERENCES DimDate(date_id)
);
