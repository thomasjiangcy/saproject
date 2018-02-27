-- SQL statements to create necessary tables

CREATE TABLE venue (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    description text,
    rating float,
    lat float,
    long float,
    thumbnail VARCHAR(255)
);

CREATE TABLE tip (
    id VARCHAR(100) PRIMARY KEY,
    venue_id VARCHAR(100) REFERENCES venue(id),
    content text
);

CREATE TABLE sentiment (
    id SERIAL PRIMARY KEY,
    tip_id VARCHAR(100) REFERENCES tip(id),
    compound float,
    positive float,
    neutral float,
    negative float
);