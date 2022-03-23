-- Who did I listen to the most this day

DROP VIEW IF EXISTS {{params.view_name}};

CREATE OR REPLACE VIEW {{params.view_name}} AS 
    SELECT s.artist_name, COUNT(1) AS num_listened
    FROM {{params.tbl_name}} AS s 
    GROUP BY s.artist_name 
    ORDER BY num_listened DESC LIMIT 5;