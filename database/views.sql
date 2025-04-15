-- View: geographical_unit_view
-- Unifies cities, districts, and neighbourhoods into a single structure
-- Useful for joining with indicators and point_features using (geo_level_id, geo_id)

CREATE OR REPLACE VIEW geographical_unit_view AS
SELECT
    1 AS geo_level_id, -- Level 1: City
    c.id AS geo_id,
    c.name AS name,
    NULL::INTEGER AS code,
    NULL::INTEGER AS parent_id,
    c.created_at,
    c.updated_at
FROM cities c

UNION ALL

SELECT
    2 AS geo_level_id, -- Level 2: District
    d.id AS geo_id,
    d.name AS name,
    d.district_code AS code,
    d.city_id AS parent_id, -- Reference to parent city
    d.created_at,
    d.updated_at
FROM districts d

UNION ALL

SELECT
    3 AS geo_level_id, -- Level 3: Neighbourhood
    n.id AS geo_id,
    n.name AS name,
    n.neighbourhood_code AS code,
    n.district_id AS parent_id, -- Reference to parent district
    n.created_at,
    n.updated_at
FROM neighbourhoods n;
