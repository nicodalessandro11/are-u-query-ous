-- Note: PostGIS extension must be enabled in Supabase dashboard first
-- Database -> Extensions -> PostGIS

-- Set search path to include public schema
SET search_path TO public;

-- Enable PostGIS extension in public schema explicitly
DROP EXTENSION IF EXISTS postgis CASCADE;
CREATE EXTENSION postgis SCHEMA public;

-- === Table: cities ===
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === Table: geographical_levels ===
CREATE TABLE geographical_levels (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === Table: districts ===
CREATE TABLE districts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    district_code INTEGER NOT NULL,
    city_id INTEGER REFERENCES cities(id) ON DELETE CASCADE,
    geom GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city_id, district_code),
    UNIQUE(city_id, name)
);

-- === Table: neighbourhoods ===
CREATE TABLE neighbourhoods (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    neighbourhood_code INTEGER NOT NULL,
    district_id INTEGER REFERENCES districts(id) ON DELETE CASCADE,
    city_id INTEGER REFERENCES cities(id) ON DELETE CASCADE,
    geom GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(district_id, neighbourhood_code),
    UNIQUE(district_id, name)
);

-- === Table: indicator_definitions ===
CREATE TABLE indicator_definitions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    unit TEXT,
    description TEXT,
    category TEXT,
    source JSONB DEFAULT '{}'::JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- === Table: indicators ===
CREATE TABLE indicators (
    id SERIAL PRIMARY KEY,
    indicator_def_id INTEGER REFERENCES indicator_definitions(id) ON DELETE CASCADE,
    geo_level_id INTEGER REFERENCES geographical_levels(id),
    geo_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    value DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(indicator_def_id, geo_level_id, geo_id, year)
);

-- === Table: feature_definitions ===
CREATE TABLE feature_definitions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === Table: point_features ===
CREATE TABLE point_features (
    id SERIAL PRIMARY KEY,
    feature_definition_id INTEGER REFERENCES feature_definitions(id) ON DELETE SET NULL,
    name TEXT,
    latitude DECIMAL NOT NULL,
    longitude DECIMAL NOT NULL,
    geom GEOMETRY(POINT, 4326),
    geo_level_id INTEGER REFERENCES geographical_levels(id),
    geo_id INTEGER NOT NULL,
    properties JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === Indexes ===
CREATE INDEX idx_indicators_geo ON indicators (geo_level_id, geo_id);
CREATE INDEX idx_point_features_geo ON point_features (geo_level_id, geo_id);
CREATE INDEX idx_point_features_definition ON point_features (feature_definition_id);

-- === Permissions ===
GRANT USAGE ON SCHEMA public TO service_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO service_role;

GRANT USAGE ON SCHEMA public TO anon;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO anon;

-- Insert permissions for specific tables (excluding PostGIS system tables)
GRANT INSERT ON cities TO service_role;
GRANT INSERT ON districts TO service_role;
GRANT INSERT ON neighbourhoods TO service_role;
GRANT INSERT ON point_features TO service_role;
GRANT INSERT ON feature_definitions TO service_role;
GRANT INSERT ON indicator_definitions TO service_role;
GRANT INSERT ON indicators TO service_role;

-- Sequence access
GRANT USAGE, SELECT ON SEQUENCE cities_id_seq TO service_role;
GRANT USAGE, SELECT ON SEQUENCE districts_id_seq TO service_role;
GRANT USAGE, SELECT ON SEQUENCE neighbourhoods_id_seq TO service_role;
GRANT USAGE, SELECT ON SEQUENCE point_features_id_seq TO service_role;
GRANT USAGE, SELECT ON SEQUENCE feature_definitions_id_seq TO service_role;
GRANT USAGE, SELECT ON SEQUENCE indicator_definitions_id_seq TO service_role;
GRANT USAGE, SELECT ON SEQUENCE indicators_id_seq TO service_role;

-- === RLS (Row-Level Security) Activation ===
ALTER TABLE cities ENABLE ROW LEVEL SECURITY;
ALTER TABLE districts ENABLE ROW LEVEL SECURITY;
ALTER TABLE neighbourhoods ENABLE ROW LEVEL SECURITY;
ALTER TABLE geographical_levels ENABLE ROW LEVEL SECURITY;
ALTER TABLE indicator_definitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE indicators ENABLE ROW LEVEL SECURITY;
ALTER TABLE feature_definitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE point_features ENABLE ROW LEVEL SECURITY;

-- === RLS Policies ===
CREATE POLICY "Service role access on cities"
  ON cities FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role access on districts"
  ON districts FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role access on neighbourhoods"
  ON neighbourhoods FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role access on geographical_levels"
  ON geographical_levels FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role access on indicator_definitions"
  ON indicator_definitions FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role access on indicators"
  ON indicators FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role access on feature_definitions"
  ON feature_definitions FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role access on point_features"
  ON point_features FOR ALL TO service_role USING (true) WITH CHECK (true);
