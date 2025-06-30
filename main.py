from config import BATCH_SIZE
from db.connect import (
    create_database_if_not_exists,
    get_source_connection,
    get_target_connection
)
from db.schema import (
    create_newspapers_table,
    create_countries_table,
    create_grade_types_table,
    create_tags_table,
    create_articles_table,
    create_article_tags_table
)
from extract.reader import read_table_in_batches
from transform.logic import (
    transform_newspaper_record,
    transform_country_records,
    transform_article_record
)
from load.loader import (
    insert_newspapers,
    insert_countries,
    insert_grade_types,
    insert_tags,
    insert_articles,
    insert_article_tags
)
from load.views import create_views
from tqdm import tqdm


if __name__ == '__main__':
    # Step 1 - Create the target database if it does not exist
    create_database_if_not_exists()

    # Step 2 - Establish source and target database connections
    source_conn = get_source_connection()
    source_cursor = source_conn.cursor(dictionary=True)
    target_conn = get_target_connection()
    target_cursor = target_conn.cursor()

    # Step 3 - Create required tables in the target database
    create_countries_table(target_cursor)
    create_newspapers_table(target_cursor)
    create_grade_types_table(target_cursor)
    create_tags_table(target_cursor)
    create_articles_table(target_cursor)
    create_article_tags_table(target_cursor)
    target_conn.commit()

    # Step 4 - Insert enum values (grade types and tags)
    insert_grade_types(target_cursor)
    insert_tags(target_cursor)
    target_conn.commit()

    # Step 5 - ETL for countries
    source_cursor.execute("SELECT * FROM countryCounts")
    raw_countries = source_cursor.fetchall()
    transformed_countries = transform_country_records(raw_countries)
    insert_countries(target_cursor, transformed_countries)
    target_conn.commit()

    # Step 6 - ETL for newspapers
    target_cursor_dict = target_conn.cursor(dictionary=True)
    target_cursor_dict.execute("SELECT name, id FROM countries")
    country_map = {row["name"]: row["id"] for row in target_cursor_dict.fetchall()}
    target_cursor_dict.close()

    for batch in read_table_in_batches(source_cursor, "newspapers", BATCH_SIZE):
        transformed = [transform_newspaper_record(row, country_map) for row in batch]
        transformed = [t for t in transformed if t is not None]
        insert_newspapers(target_cursor, transformed)
        target_conn.commit()

    # Step 7 - ETL for articles (merge graded and ungraded articles)
    source_cursor.execute("SELECT * FROM articles")
    graded_articles = source_cursor.fetchall()
    source_cursor.execute("SELECT * FROM ungradedArticles")
    ungraded_articles = source_cursor.fetchall()
    all_articles = [(row, True) for row in graded_articles] + [(row, False) for row in ungraded_articles]

    # Load reference mappings
    target_cursor_dict = target_conn.cursor(dictionary=True)
    target_cursor_dict.execute("SELECT type, id FROM gradeTypes")
    grade_type_table = {row["type"]: row["id"] for row in target_cursor_dict.fetchall()}

    target_cursor_dict.execute("SELECT name, id FROM countries")
    country_map = {row["name"]: row["id"] for row in target_cursor_dict.fetchall()}

    target_cursor_dict.execute("SELECT name, id FROM newspapers")
    newspaper_map = {row["name"]: row["id"] for row in target_cursor_dict.fetchall()}
    target_cursor_dict.close()

    # Transform articles
    target_cursor_dict = target_conn.cursor(dictionary=True)
    transformed_articles = []
    for row, flag in tqdm(all_articles, desc="Transformation articles", unit="article"):
        transformed = transform_article_record(
            row,
            grade_type_table,
            country_map,
            newspaper_map,
            tag_list_enabled=flag,
            db_cursor=target_cursor_dict
        )
        if transformed:
            transformed_articles.append(transformed)
    transformed_articles = [a for a in transformed_articles if a is not None]
    target_cursor_dict.close()

    # Load tag mappings
    target_cursor_dict = target_conn.cursor(dictionary=True)
    target_cursor_dict.execute("SELECT name, id FROM tags")
    tag_map = {row["name"]: row["id"] for row in target_cursor_dict.fetchall()}
    target_cursor_dict.close()

    # Insert articles and tags into target database
    insert_articles(target_cursor, transformed_articles)
    target_conn.commit()

    insert_article_tags(target_cursor, transformed_articles, tag_map)
    target_conn.commit()

    # Step 8 - Create database views
    create_views(target_cursor)
    target_conn.commit()

    # Step 9 - Cleanup connections and cursors
    source_cursor.close()
    target_cursor.close()
    source_conn.close()
    target_conn.close()
