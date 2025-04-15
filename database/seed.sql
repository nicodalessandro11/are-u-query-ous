-- === Seed script for initial data ===

-- Insert cities
INSERT INTO cities (name) VALUES
    ('Barcelona'),
    ('Madrid');

-- Insert geographical levels
-- 1: City, 2: District, 3: Neighbourhood
INSERT INTO geographical_levels (name) VALUES
    ('City'),
    ('District'),
    ('Neighbourhood');
