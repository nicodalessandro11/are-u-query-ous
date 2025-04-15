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

-- Insert feature types (used in point_features.feature_type_id)
INSERT INTO feature_types (name, description) VALUES
    ('Bibliotecas', 'Bibliotecas públicas y centros de documentación'),
    ('Centros culturales', 'Ateneos, centros cívicos y espacios culturales de uso comunitario'),
    ('Auditorios', 'Grandes auditorios y salas de conciertos'),
    ('Espacios patrimoniales', 'Lugares de interés histórico, cultural o patrimonial'),
    ('Fábricas de creación', 'Centros de innovación cultural y artística'),
    ('Museos', 'Museos y colecciones permanentes'),
    ('Cines', 'Salas de cine comerciales o culturales'),
    ('Centros de exposiciones', 'Espacios destinados a exposiciones artísticas o temáticas'),
    ('Archivos', 'Archivos históricos, distritales y bibliotecas patrimoniales'),
    ('Salas de música en vivo', 'Salas destinadas a conciertos y actuaciones musicales'),
    ('Salas de artes escénicas', 'Teatros y espacios para espectáculos escénicos');
