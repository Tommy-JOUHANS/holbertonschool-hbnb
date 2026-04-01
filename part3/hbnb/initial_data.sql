INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin', 'HBnB', 'admin@hbnb.io',
    '$2b$12$bnkulHyYHLXJA2DJZ9Z/hOorKdLWSPOuYjN4MOwzglA8xuQR3XA1a',
    1,
    datetime('now'), datetime('now')
);

INSERT INTO amenities (id, name, created_at, updated_at) VALUES
    ('22cff317-1586-4b5d-a202-6a39c5733a60', 'WiFi',          datetime('now'), datetime('now')),    
    ('2b1c8e5e-9a3b-4c8f-9d1e-5f0a7c9e8b2d', 'Télévision',     datetime('now'), datetime('now')),    
    ('3c2d9f4a-7e5b-4a6c-8f1d-4e0b6a7c9d3f', 'Cuisine équipée', datetime('now'), datetime('now')),
    ('39ade721-042c-4efd-b6b2-8066c82ddcab', 'Piscine',       datetime('now'), datetime('now')),
    ('6a011a31-c18a-4b52-bba3-c052c1b2b099', 'Climatisation', datetime('now'), datetime('now'));    
