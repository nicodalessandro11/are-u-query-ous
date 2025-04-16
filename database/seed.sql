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

-- Insert feature definitions (used in point_features.feature_type_id)
INSERT INTO feature_definitions (name, description) VALUES
    ('Libraries', 'Public libraries and documentation centers'),
    ('Cultural centers', 'Athenaeums, civic centers and community cultural spaces'),
    ('Auditoriums', 'Large auditoriums and concert halls'),
    ('Heritage spaces', 'Places of historical, cultural or heritage interest'),
    ('Creation factories', 'Cultural and artistic innovation centers'),
    ('Museums', 'Museums and permanent collections'),
    ('Cinemas', 'Commercial or cultural movie theaters'),
    ('Exhibition centers', 'Spaces for artistic or thematic exhibitions'),
    ('Archives', 'Historical, district archives and heritage libraries'),
    ('Live music venues', 'Venues for concerts and musical performances'),
    ('Performing arts venues', 'Theaters and spaces for stage performances');

-- Insert indicator definitions (used in indicators.indicator_def_id)
INSERT INTO indicator_definitions (name, description, unit) VALUES
    ('Population', 'Total population of the city', 'inhabitants'),
    ('Population density', 'Population density of the city', 'inhabitants per square kilometer'),
    ('Average gross household income', 'Average gross household income per neighborhood, calculated as the mean of census section values', 'euros');

