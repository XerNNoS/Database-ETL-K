def create_views(cursor):
    # View 1 — Enriched articles with readable names
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

    # View 2 — Number of articles per grade type
    cursor.execute("""
    CREATE OR REPLACE VIEW article_counts_by_grade AS
    SELECT
        gt.type AS grade_type,
        COUNT(*) AS article_count
    FROM articles a
    JOIN gradeTypes gt ON a.gradeType_id = gt.id
    GROUP BY gt.type;
    """)

    # View 3 — Number of articles per country
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

    # View 4 — Number of articles per newspaper with readable names
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

    # View 5 — Flattened tags per article
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

    # View 6 — Aggregated list of tags per article
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

    # View 7 — Number of articles per tag
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

    # View 8 — Articles with tags (aggregated)
    cursor.execute("""
    CREATE OR REPLACE VIEW articles_with_tags AS
    SELECT
        af.*,
        at.tags
    FROM articles_full af
    LEFT JOIN article_tags_aggregated at ON af.id = at.article_id;
    """)

    # View 9 — Summary of articles per grade by month and newspaper
    cursor.execute("""
    CREATE OR REPLACE VIEW article_grades_summary AS
    SELECT
        CAST(DATE_FORMAT(a.pubDate, '%Y-%m') AS CHAR) COLLATE utf8mb4_general_ci AS year_month_period,
        n.id AS newspaper_id,
        SUM(CASE WHEN gt.type = 'neutral' THEN 1 ELSE 0 END) AS neutral,
        SUM(CASE WHEN gt.type = 'positive' THEN 1 ELSE 0 END) AS positive,
        SUM(CASE WHEN gt.type = 'negative' THEN 1 ELSE 0 END) AS negative,
        SUM(CASE WHEN gt.type IN ('neutral', 'positive', 'negative') THEN 1 ELSE 0 END) AS `ALL`
    FROM articles a
    JOIN gradeTypes gt ON a.gradeType_id = gt.id
    JOIN newspapers n ON a.newspaper_id = n.id
    WHERE a.pubDate IS NOT NULL
    AND gt.type IN ('neutral', 'positive', 'negative')
    GROUP BY year_month_period, n.id

    UNION ALL

    SELECT
        CAST('all_time' AS CHAR) COLLATE utf8mb4_general_ci AS year_month_period,
        n.id AS newspaper_id,
        SUM(CASE WHEN gt.type = 'neutral' THEN 1 ELSE 0 END) AS neutral,
        SUM(CASE WHEN gt.type = 'positive' THEN 1 ELSE 0 END) AS positive,
        SUM(CASE WHEN gt.type = 'negative' THEN 1 ELSE 0 END) AS negative,
        SUM(CASE WHEN gt.type IN ('neutral', 'positive', 'negative') THEN 1 ELSE 0 END) AS `ALL`
    FROM articles a
    JOIN gradeTypes gt ON a.gradeType_id = gt.id
    JOIN newspapers n ON a.newspaper_id = n.id
    WHERE a.pubDate IS NOT NULL
    AND gt.type IN ('neutral', 'positive', 'negative')
    GROUP BY n.id;
    """)

    # View 10 — Raw article data with readable labels (original version)
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
    LEFT JOIN newspapers np ON a.newspaper_id = np.id;
    """)
