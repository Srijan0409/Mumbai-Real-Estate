-- SQL Script: Analysis Queries for Real Estate Database
-- Database: real_estate

USE real_estate;

-- 1. Average price per sqft by region, sorted descending
-- Answers: Which regions have the highest property valuation per square foot?
SELECT 
    region, 
    ROUND(AVG(price_per_sqft), 2) AS avg_price_per_sqft,
    COUNT(*) AS total_listings
FROM properties
GROUP BY region
ORDER BY avg_price_per_sqft DESC;


-- 2. Top 10 most expensive localities by average price
-- Answers: What are the top 10 most premium micro-markets (localities) in terms of average listing price?
SELECT 
    locality, 
    region, 
    ROUND(AVG(price_in_lakhs), 2) AS avg_price_in_lakhs,
    COUNT(*) AS listing_count
FROM properties
GROUP BY locality, region
ORDER BY avg_price_in_lakhs DESC
LIMIT 10;


-- 3. Average price by BHK type
-- Answers: How does the pricing scale with the number of bedrooms (BHK)?
SELECT 
    bhk, 
    ROUND(AVG(price_in_lakhs), 2) AS avg_price_in_lakhs,
    COUNT(*) AS listing_count
FROM properties
GROUP BY bhk
ORDER BY bhk;


-- 4. Count of listings by status (Ready to Move vs Under Construction) per region
-- Answers: What is the distribution of inventory availability (ready vs under construction) across different regions?
SELECT 
    region, 
    status, 
    COUNT(*) AS listing_count
FROM properties
GROUP BY region, status
ORDER BY region, status;


-- 5. Average area and price for each property type
-- Answers: What are the average dimensions (sqft) and typical listing prices for different typologies (e.g., Apartment, Villa, Studio)?
SELECT 
    type, 
    ROUND(AVG(area), 2) AS avg_area_sqft, 
    ROUND(AVG(price_in_lakhs), 2) AS avg_price_in_lakhs,
    COUNT(*) AS listing_count
FROM properties
GROUP BY type
ORDER BY avg_price_in_lakhs DESC;


-- 6. Regions with the highest number of listings
-- Answers: Which geographic regions dominate the real estate market in terms of listing volume?
SELECT 
    region, 
    COUNT(*) AS listing_count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM properties)), 2) AS market_share_percentage
FROM properties
GROUP BY region
ORDER BY listing_count DESC;


-- 7. Price range (min/max/avg) grouped by BHK
-- Answers: What is the spread of listing prices (minimum, maximum, average) across different BHK configurations?
SELECT 
    bhk, 
    MIN(price_in_lakhs) AS min_price_in_lakhs, 
    MAX(price_in_lakhs) AS max_price_in_lakhs, 
    ROUND(AVG(price_in_lakhs), 2) AS avg_price_in_lakhs,
    COUNT(*) AS listing_count
FROM properties
GROUP BY bhk
ORDER BY bhk;
