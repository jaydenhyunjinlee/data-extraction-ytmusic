-- How many songs did I play "TODAY" or `played_on` = 'Today'

DROP VIEW IF EXISTS {{params.view_name}};

CREATE OR REPLACE VIEW {{params.view_name}} AS 
    SELECT COUNT(DISTINCT song_name) AS num_played_today
    FROM {{params.tbl_name}}
    WHERE UPPER(played_on) = 'TODAY';