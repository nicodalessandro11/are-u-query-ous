-- Enable PostGIS extension for spatial geometry support
CREATE EXTENSION IF NOT EXISTS postgis;

-- Table: cities
-- Stores supported cities (e.g., Madrid, Barcelona)
CREATE TABLE
    cities (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- Table: geographical_levels
-- Defines the level of geography (city, district, neighbourhood, etc.)
CREATE TABLE
    geographical_levels (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- Table: districts
-- Stores districts within a city, each with a unique code per city
CREATE TABLE
    districts (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        district_code INTEGER NOT NULL, -- e.g., 1, 5
        city_id INTEGER REFERENCES cities (id) ON DELETE CASCADE,
        geom GEOMETRY (POLYGON, 4326), -- District geometry in WGS84
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (city_id, district_code), -- Ensures district_code is unique per city
        UNIQUE (city_id, name) -- Prevents duplicate district names per city
    );

-- Table: neighbourhoods
-- Stores neighbourhoods within a district, each with a unique code per district and explicit city reference
CREATE TABLE
    neighbourhoods (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        neighbourhood_code INTEGER NOT NULL, -- e.g., 1, 3
        district_id INTEGER REFERENCES districts (id) ON DELETE CASCADE,
        city_id INTEGER REFERENCES cities (id) ON DELETE CASCADE, -- NEW: explicit reference to city
        geom GEOMETRY (POLYGON, 4326), -- Neighbourhood geometry in WGS84
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (district_id, neighbourhood_code), -- Ensures neighbourhood_code is unique per district
        UNIQUE (district_id, name)                -- Prevents duplicate names per district
    );

-- Table: indicator_definitions
-- Defines what each indicator measures (e.g., population, average income)
CREATE TABLE
    indicator_definitions (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        unit TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- Table: indicators
-- Stores the values of each indicator for a given area and year
CREATE TABLE
    indicators (
        id SERIAL PRIMARY KEY,
        indicator_def_id INTEGER REFERENCES indicator_definitions (id) ON DELETE CASCADE,
        geo_level_id INTEGER REFERENCES geographical_levels (id),
        geo_id INTEGER NOT NULL, -- Refers to city/district/neighbourhood ID depending on geo_level_id
        year INTEGER NOT NULL,
        value DECIMAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (indicator_def_id, geo_level_id, geo_id, year)
    );

-- Table: point_features
-- Stores individual geolocated features (e.g., schools, hospitals)
CREATE TABLE
    point_features (
        id SERIAL PRIMARY KEY,
        feature_type TEXT NOT NULL, -- e.g., "school", "park"
        name TEXT,
        latitude DECIMAL NOT NULL,
        longitude DECIMAL NOT NULL,
        geom GEOMETRY (POINT, 4326),
        geo_level_id INTEGER REFERENCES geographical_levels (id),
        geo_id INTEGER NOT NULL,
        properties JSONB, -- Stores feature attributes in JSON format
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- Indexes for improved query performance
CREATE INDEX idx_indicators_geo ON indicators (geo_level_id, geo_id);

CREATE INDEX idx_point_features_geo ON point_features (geo_level_id, geo_id);

CREATE INDEX idx_point_features_type ON point_features (feature_type);

-- 🔓 TEMPORARY PERMISSIONS FOR INGEST SCRIPT (commented out by default)
-- These lines allow read access for the Supabase service role to run the ETL script.
-- Uncomment if you run this project in a Supabase environment.

GRANT USAGE ON SCHEMA public TO service_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO service_role;

GRANT USAGE ON SCHEMA public TO anon;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO anon;

GRANT INSERT ON TABLE public.districts TO service_role;
GRANT INSERT ON TABLE public.neighbourhoods TO service_role;

GRANT USAGE, SELECT ON SEQUENCE districts_id_seq TO service_role;
GRANT USAGE, SELECT ON SEQUENCE neighbourhoods_id_seq TO service_role;
