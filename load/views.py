def create_views(cursor):
    # Vue 1 — Articles enrichis avec noms lisibles
    cursor.execute("""
    CREATE OR REPLACE VIEW articles_full AS
    SELECT
        a.id,
        a.title,
        a.link,
        a.pubDate,
        gt.type AS grade_type,
        np.name AS newspaper_name,
        c.id AS country_id,
        a.original_language,
        a.translated_title,
        a.translated_article,
        a.image_link,
        a.moderator,
        a.gradeDate
    FROM articles a
    LEFT JOIN gradeTypes gt ON a.gradeType_id = gt.id
    LEFT JOIN newspapers np ON a.newspaper_id = np.id
    LEFT JOIN countries c ON a.country_id = c.id;
    """)

    # Vue 2 — Nombre d'articles par grade global
    cursor.execute("""
    CREATE OR REPLACE VIEW article_counts_by_grade AS
    SELECT
        gt.type AS grade_type,
        COUNT(*) AS article_count
    FROM articles a
    JOIN gradeTypes gt ON a.gradeType_id = gt.id
    GROUP BY gt.type;
    """)

    # Vue 3 — Nombre d'articles par country (avec leur nom)
    cursor.execute("""
    CREATE OR REPLACE VIEW article_counts_by_country AS
    SELECT
        c.name AS country,
        COUNT(*) AS article_count
    FROM articles a
    JOIN countries c ON a.country_id = c.id
    GROUP BY c.name
    ORDER BY article_count DESC;
    """)

    # Vue 4 — Nombre d'articles par newspaper (avec noms lisibles)
    cursor.execute("""
    CREATE OR REPLACE VIEW article_counts_by_newspaper AS
    SELECT
        np.name AS newspaper_name,
        c.name AS country,
        COUNT(*) AS article_count
    FROM articles a
    JOIN newspapers np ON a.newspaper_id = np.id
    LEFT JOIN countries c ON np.country_id = c.id
    GROUP BY newspaper_name, country
    ORDER BY article_count DESC;
    """)

    # Vue 5 — Tags par article (flattened)
    cursor.execute("""
    CREATE OR REPLACE VIEW article_tags_flat AS
    SELECT
        a.id AS article_id,
        a.title,
        t.name AS tag
    FROM articles a
    JOIN articleTags at ON a.id = at.article_id
    JOIN tags t ON at.tag_id = t.id;
    """)

    # Vue 6 — Liste des tags par article (agrégée)
    cursor.execute("""
    CREATE OR REPLACE VIEW article_tags_aggregated AS
    SELECT
        a.id AS article_id,
        a.title,
        GROUP_CONCAT(t.name ORDER BY t.name SEPARATOR ', ') AS tags
    FROM articles a
    JOIN articleTags at ON a.id = at.article_id
    JOIN tags t ON at.tag_id = t.id
    GROUP BY a.id, a.title;
    """)

    # Vue 7 — Nombre d'articles par tag
    cursor.execute("""
    CREATE OR REPLACE VIEW tag_counts AS
    SELECT
        t.name AS tag,
        COUNT(at.article_id) AS article_count
    FROM articleTags at
    JOIN tags t ON at.tag_id = t.id
    GROUP BY t.name
    ORDER BY article_count DESC;
    """)

    # Vue 8 — Articles avec tous les tags et noms joints (agrégé)
    cursor.execute("""
    CREATE OR REPLACE VIEW articles_with_tags AS
    SELECT
        af.*,
        at.tags
    FROM articles_full af
    LEFT JOIN article_tags_aggregated at ON af.id = at.article_id;
    """)

    # Vue 9 - Custom
    cursor.execute("""
    CREATE OR REPLACE VIEW article_grades_summary AS
    SELECT
        -- Extract year and month
        CAST(DATE_FORMAT(a.pubDate, '%Y-%m') AS CHAR) COLLATE utf8mb4_general_ci AS year_month_period,

        -- Newspaper info
        n.id AS newspaper_id,

        -- Count of article by grade type (Neutral, Positive, Negative)
        SUM(CASE WHEN gt.type = 'Neutral' THEN 1 ELSE 0 END) AS Neutral,
        SUM(CASE WHEN gt.type = 'Positive' THEN 1 ELSE 0 END) AS Positive,
        SUM(CASE WHEN gt.type = 'Negative' THEN 1 ELSE 0 END) AS Negative,

        -- Sum of the three
        SUM(CASE WHEN gt.type IN ('Neutral', 'Positive', 'Negative') THEN 1 ELSE 0 END) AS `ALL`

    FROM articles a
    JOIN gradeTypes gt ON a.gradeType_id = gt.id
    JOIN newspapers n ON a.newspaper_id = n.id
    
    WHERE a.pubDate IS NOT NULL
    AND gt.type IN ('Neutral', 'Positive', 'Negative')

    GROUP BY year_month_period, n.id

    UNION ALL

    -- ALL_TIME summary (no date restriction)
    SELECT
        CAST('ALL_TIME' AS CHAR) COLLATE utf8mb4_general_ci AS year_month_period
 ,

        n.id AS newspaper_id,

        SUM(CASE WHEN gt.type = 'Neutral' THEN 1 ELSE 0 END) AS Neutral,
        SUM(CASE WHEN gt.type = 'Positive' THEN 1 ELSE 0 END) AS Positive,
        SUM(CASE WHEN gt.type = 'Negative' THEN 1 ELSE 0 END) AS Negative,

        SUM(CASE WHEN gt.type IN ('Neutral', 'Positive', 'Negative') THEN 1 ELSE 0 END) AS `ALL`

    FROM articles a
    JOIN gradeTypes gt ON a.gradeType_id = gt.id
    JOIN newspapers n ON a.newspaper_id = n.id

    WHERE a.pubDate IS NOT NULL
    AND gt.type IN ('Neutral', 'Positive', 'Negative')

    GROUP BY n.id
    """)


    cursor.execute("""
        CREATE OR REPLACE VIEW article_original AS
        SELECT
        a.id,
        a.title,
        a.link,
        a.pubDate,
        gt.type AS grade_type,
        np.name AS newspaper_name,
        a.country_id,
        a.original_language,
        a.translated_title,
        a.translated_article,
        a.image_link,
        a.moderator,
        a.gradeDate
        FROM articles a
        LEFT JOIN gradeTypes gt ON a.gradeType_id = gt.id
        LEFT JOIN newspapers np ON a.newspaper_id = np.id
    """)