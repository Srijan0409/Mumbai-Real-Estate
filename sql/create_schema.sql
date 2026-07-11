-- SQL Script: Create Schema for Real Estate Price Analysis
-- Database name: real_estate
-- Table name: properties

CREATE DATABASE IF NOT EXISTS real_estate;
USE real_estate;

DROP TABLE IF EXISTS properties;

CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bhk INT,
    type VARCHAR(100),
    locality VARCHAR(255),
    area DOUBLE,
    price DOUBLE,
    price_unit VARCHAR(10),
    region VARCHAR(100),
    status VARCHAR(50),
    age VARCHAR(50),
    price_in_lakhs DOUBLE,
    price_per_sqft DOUBLE
);
