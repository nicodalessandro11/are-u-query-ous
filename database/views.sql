-- === Views Definition ===

-- Drop existing view to prevent column name conflicts
DROP VIEW IF EXISTS geographical_unit_view;

-- View: geographical_unit_view
-- Unifies cities, districts, and neighbourhoods into a single structure
-- Useful for joining with indicators and point_features using (geo_level_id, geo_id)
-- Includes `city_id` explicitly for easier filtering and joins

CREATE OR REPLACE VIEW geographical_unit_view AS
-- Cities (Level 1)
SELECT
    1 AS geo_level_id,            -- 1: City
    c.id AS geo_id,               -- Unique ID of the city
    c.name AS name,               -- City name
    NULL::INTEGER AS code,        -- No code at city level
    NULL::INTEGER AS parent_id,   -- No parent
    c.id AS city_id,              -- Self-reference for city-level
    c.created_at,
    c.updated_at
FROM cities c

UNION ALL

-- Districts (Level 2)
SELECT
    2 AS geo_level_id,            -- 2: District
    d.id AS geo_id,               -- Unique ID of the district
    d.name AS name,               -- District name
    d.district_code AS code,      -- District code (e.g., 1, 2, ...)
    d.city_id AS parent_id,       -- Points to parent city
    d.city_id AS city_id,         -- City reference
    d.created_at,
    d.updated_at
FROM districts d

UNION ALL

-- Neighbourhoods (Level 3)
SELECT
    3 AS geo_level_id,            -- 3: Neighbourhood
    n.id AS geo_id,               -- Unique ID of the neighbourhood
    n.name AS name,               -- Neighbourhood name
    n.neighbourhood_code AS code,-- Neighbourhood code
    n.district_id AS parent_id,   -- Points to parent district
    n.city_id AS city_id,         -- City reference (explicit)
    n.created_at,
    n.updated_at
FROM neighbourhoods n;
