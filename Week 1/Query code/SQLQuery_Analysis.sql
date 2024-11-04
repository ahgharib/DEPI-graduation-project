use Feedback_Project1

-- Total Number of Feedback Entries
SELECT COUNT(*) AS total_feedback
FROM Feedback;

-- Average Rating by Store --
SELECT s.id AS store_id, s.addresses, AVG(f.rating) AS average_rating
FROM Feedback f
JOIN Store s ON f.store_id = s.id
GROUP BY s.id, s.addresses
ORDER BY average_rating DESC;

-- Total Feedback Count by Store
SELECT s.id AS store_id, s.addresses, COUNT(f.id) AS feedback_count
FROM Feedback f
JOIN Store s ON f.store_id = s.id
GROUP BY s.id, s.addresses
ORDER BY feedback_count DESC;

-- Rating of each customer
SELECT c.id AS customer_id, c.names, f.rating AS rating
FROM Feedback f
JOIN Customer c ON f.customer_id = c.id
ORDER BY rating DESC;


-- Monthly Feedback Count Over Time
SELECT YEAR(dates) AS year, MONTH(dates) AS month, COUNT(*) AS feedback_count
FROM Orders o
JOIN Feedback f ON o.id = f.order_id
GROUP BY YEAR(dates), MONTH(dates)
ORDER BY year, month;

-- Average Rating Over Time
SELECT YEAR(dates) AS year, MONTH(dates) AS month, AVG(f.rating) AS average_rating
FROM Orders o
JOIN Feedback f ON o.id = f.order_id
GROUP BY YEAR(dates), MONTH(dates)
ORDER BY year, month;


-- Feedback Distribution by Rating
SELECT rating, COUNT(*) AS count
FROM Feedback
GROUP BY rating
ORDER BY rating;

-- Top Products by Average Rating
SELECT p.id AS product_id, p.names, AVG(f.rating) AS average_rating
FROM OrderDetails od
JOIN Feedback f ON od.order_id = f.order_id
JOIN Product p ON od.product_id = p.id
GROUP BY p.id, p.names
ORDER BY average_rating DESC;

-- Feedback Sentiment Analysis (simplistic sentiment classification based on keywords)
SELECT 
    CASE 
        WHEN review LIKE '%good%' THEN 'Positive'
        WHEN review LIKE '%bad%' THEN 'Negative'
        ELSE 'Neutral'
    END AS sentiment,
    COUNT(*) AS count
FROM Feedback
GROUP BY 
    CASE 
        WHEN review LIKE '%good%' THEN 'Positive'
        WHEN review LIKE '%bad%' THEN 'Negative'
        ELSE 'Neutral'
    END;



-- Average Rating for All Customers
SELECT AVG(f.rating) AS overall_average_rating
FROM Feedback f;


-- Store Performance Comparison
SELECT s.id AS store_id, s.addresses, AVG(f.rating) AS average_rating, COUNT(f.id) AS feedback_count, (COUNT(f.id)/AVG(f.rating))as ratio
FROM Feedback f
JOIN Store s ON f.store_id = s.id
GROUP BY s.id, s.addresses
ORDER BY ratio DESC, average_rating DESC, feedback_count DESC;

/*
-- Detailed Feedback Entries for a Specific Store
SELECT f.review, f.rating, c.names
FROM Feedback f
JOIN Customer c ON f.customer_id = c.id
WHERE f.store_id = 1;  -- Replace 1 with the desired store_ID
*/

-- Detailed Feedback Entries for a Specific Store
SELECT f.review, f.rating, c.names
FROM Feedback f
JOIN Customer c ON f.customer_id = c.id
JOIN Store s ON f.store_id = s.id  -- Join with Store table
WHERE f.store_id = 1  -- Replace 1 with the desired store_ID
ORDER BY f.rating DESC;



-- Feedback with Ratings Lower than Average
SELECT f.review, f.rating, s.addresses
FROM Feedback f
JOIN Store s ON f.store_id = s.id
WHERE f.rating < (
    SELECT AVG(rating) FROM Feedback
);

-- Feedback with Ratings Higher than Average
SELECT f.review, f.rating, s.addresses
FROM Feedback f
JOIN Store s ON f.store_id = s.id
WHERE f.rating > (
    SELECT AVG(rating) FROM Feedback
);



-- Calculate Total Amount of Price per Each Order
CREATE VIEW TotalOrderAmount AS
SELECT 
    O.id AS order_id,
    SUM(P.price * OD.quantity) AS total_price
FROM 
    Orders O
JOIN 
    OrderDetails OD ON O.id = OD.order_id
JOIN 
    Product P ON OD.product_id = P.id
GROUP BY 
    O.id;

-- Retrieve Total Price for Each Order
SELECT 
    *
FROM 
    TotalOrderAmount
	order by order_id asc;


-- Combine Feedback and Total Order Amount
SELECT 
    F.id AS feedback_id,
    F.review,
    F.rating,
    TOA.total_price,
    St.addresses AS store_address,
    C.names AS customer_name
FROM 
    Feedback F
JOIN 
    TotalOrderAmount TOA ON F.order_id = TOA.order_id
JOIN 
    Orders O ON F.order_id = O.id
JOIN 
    Store St ON O.store_id = St.id
JOIN 
    Customer C ON F.customer_id = C.id;




-- Feedback analysis function
CREATE FUNCTION dbo.GetFeedbackCategory (@rating INT)
RETURNS VARCHAR(10)
AS
BEGIN
    DECLARE @category VARCHAR(10);

    IF @rating IS NULL
        SET @category = 'No Feedback';
    ELSE IF @rating BETWEEN 1 AND 2
        SET @category = 'negative';
    ELSE IF @rating = 3
        SET @category = 'neutral';
    ELSE IF @rating BETWEEN 4 AND 5
        SET @category = 'positive';
    ELSE
        SET @category = 'Invalid Rating';

    RETURN @category;
END;

-- Usage
SELECT 
    RatingValue,
    dbo.GetFeedbackCategory(RatingValue) AS FeedbackCategory
FROM 
    (VALUES (1), (2), (3), (4), (5), (NULL), (6)) AS Ratings(RatingValue);



-- Order Details With Feedback View
CREATE VIEW OrderDetailsWithFeedback AS
SELECT 
    O.id AS order_id,
    C.names AS customer_name,
    St.addresses AS store_address,
    St.rating_count AS store_rating_count,
    O.dates AS sale_date,
    P.names AS product_name,
    OD.quantity,
    P.price AS unit_price,
    (OD.quantity * P.price) AS total_price,
    F.review,
    F.rating,
    dbo.GetFeedbackCategory(F.rating) AS feedback_category,
    (SELECT SUM(OD2.quantity * P2.price)
     FROM OrderDetails OD2
     JOIN Product P2 ON OD2.product_id = P2.id
     WHERE OD2.order_id = O.id) AS total_order_price
FROM 
    Orders O
JOIN 
    Customer C ON O.customer_id = C.id
JOIN 
    Store St ON O.store_id = St.id
JOIN 
    OrderDetails OD ON O.id = OD.order_id
JOIN 
    Product P ON OD.product_id = P.id
LEFT JOIN 
    Feedback F ON O.id = F.order_id;


-- Usage:
SELECT * 
FROM OrderDetailsWithFeedback
WHERE order_id = 250; --desired order_id