-- Create the database
CREATE DATABASE Feedback_Project1;
GO

-- Use the database
USE Feedback_Project1;
GO

-- Create Customer Table with name and state columns
CREATE TABLE Customer (
    id INT IDENTITY(1,1) PRIMARY KEY,
    names VARCHAR(255) NOT NULL,
    states VARCHAR(100) NOT NULL
);

-- Import data into Customer table
BULK INSERT Customer
FROM 'C:\Users\PC\OneDrive\Desktop\SQL\Final project\DEPI\Database CSV\Customer.csv' 
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);


CREATE TABLE Store (
    id INT IDENTITY(1,1) PRIMARY KEY,
    latitude Float,
    longitude Float,
	rating_count Int,
	addresses VARCHAR(255) NOT NULL
    
);

-- Import data into Store table
BULK INSERT Store
FROM 'C:\Users\PC\OneDrive\Desktop\SQL\Final project\DEPI\Database CSV\Store_edit.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);



-- Create Product Table
CREATE TABLE Product (
    id INT IDENTITY(1,1) PRIMARY KEY,
    names VARCHAR(255),
    price FLOAT,
);


BULK INSERT Product
FROM 'C:\Users\PC\OneDrive\Desktop\SQL\Final project\DEPI\Database CSV\products.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    MAXERRORS = 1000,
    KEEPNULLS
);



-- Create Orders Table
CREATE TABLE Orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    dates DATETIME,
    customer_id INT,
    store_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(id),
    FOREIGN KEY (store_id) REFERENCES Store(id)
);


BULK INSERT Orders
FROM 'C:\Users\PC\OneDrive\Desktop\SQL\Final project\DEPI\Database CSV\sales.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    MAXERRORS = 1000,
    KEEPNULLS
);



-- Create OrderDetails Table
CREATE TABLE OrderDetails (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);


BULK INSERT OrderDetails
FROM 'C:\Users\PC\OneDrive\Desktop\SQL\Final project\DEPI\Database CSV\order_details.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    MAXERRORS = 1000,
    KEEPNULLS
);


CREATE TABLE Feedback (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    store_id INT NOT NULL,
    order_id INT NOT NULL UNIQUE,
    review TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    FOREIGN KEY (customer_id) REFERENCES Customer(id),
    FOREIGN KEY (store_id) REFERENCES Store(id),
    FOREIGN KEY (order_id) REFERENCES Orders(id)
);

BULK INSERT Feedback
FROM 'C:\Users\PC\OneDrive\Desktop\SQL\Final project\DEPI\Database CSV\Feedback_cleaned2.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    MAXERRORS = 1000,
    KEEPNULLS
);



-- deleting rating_count column
ALTER TABLE Store
DROP COLUMN rating_count;

-- Creating new rating_count column
ALTER TABLE Store
ADD rating_count INT DEFAULT 0;


-- adding the current Values to the new rating_count column
UPDATE Store
SET rating_count = (
    SELECT COALESCE(SUM(rating), 0)
    FROM Feedback
    WHERE Feedback.store_id = Store.id
);


-- Creating a TRIGGER for insertion of new data 
CREATE TRIGGER trg_InsertFeedback
ON Feedback
AFTER INSERT
AS
BEGIN
    UPDATE Store
    SET rating_count = rating_count + inserted.rating
    FROM Store
    INNER JOIN inserted ON Store.id = inserted.store_id;
END;






-- Creating a TRIGGER for Deletion of data  (No logical use for it)
CREATE TRIGGER trg_DeleteFeedback
ON Feedback
AFTER DELETE
AS
BEGIN
    UPDATE Store
    SET rating_count = rating_count - deleted.rating
    FROM Store
    INNER JOIN deleted ON Store.id = deleted.store_id;
END;




-- Creating a TRIGGER for Update on current data (No logical use for it)
CREATE TRIGGER trg_UpdateFeedback
ON Feedback
AFTER UPDATE
AS
BEGIN
    UPDATE Store
    SET rating_count = rating_count - deleted.rating + inserted.rating
    FROM Store
    INNER JOIN deleted ON Store.id = deleted.store_id
    INNER JOIN inserted ON Store.id = inserted.store_id;
END;