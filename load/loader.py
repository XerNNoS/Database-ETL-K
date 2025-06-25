def insert_users(cursor, users):
    for user in users:
        cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
            (user["username"], user["email"], user["age"])
        )


def insert_newspapers(cursor, records):
    for rec in records:
        cursor.execute("""
            INSERT INTO newspapers (
                id, name, link, country_id, monthly_readers,
                political_inclination, basic_info, logo, owner
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            rec["id"],
            rec["name"],
            rec["link"],
            rec["country_id"],
            rec["monthly_readers"],
            rec["political_inclination"],
            rec["basic_info"],
            rec["logo"],
            rec["owner"]
        ))

def insert_countries(cursor, records):
    for rec in records:
        cursor.execute("""
            INSERT INTO countries (
                id, name, flag_logo, unsc, qsd, five_eyes,
                eco_rank, diasporic_rank, border_dispute, brics,
                import_rank, export_rank, defense_rank, tourism_rank, nuclear
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s)
        """, (
            rec["id"],
            rec["name"],
            rec.get("flag_logo"),
            rec.get("unsc"),
            rec.get("qsd"),
            rec.get("five_eyes"),
            rec.get("eco_rank"),
            rec.get("diasporic_rank"),
            rec.get("border_dispute"),
            rec.get("brics"),
            rec.get("import_rank"),
            rec.get("export_rank"),
            rec.get("defense_rank"),
            rec.get("tourism_rank"),
            rec.get("nuclear")
        ))

import uuid

def insert_grade_types(cursor):
    types = ["Positive", "Negative", "Neutral", "Irrelevant", "Ungraded"]
    for t in types:
        cursor.execute("""
            INSERT INTO gradeTypes (id, type) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE type = VALUES(type)
        """, (str(uuid.uuid4()), t))


def insert_tags(cursor):
    tags = [
        "Society",
        "Geopolitics",
        "Politics",
        "Environment",
        "Business",
        "Culture",
        "Science",
        "TechScience"
    ]
    for name in tags:
        cursor.execute("""
            INSERT INTO tags (id, name) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name)
        """, (str(uuid.uuid4()), name))


def insert_articles(cursor, articles):
    for a in articles:
        cursor.execute("""
            INSERT INTO articles (
                id, title, body, link, pubDate, gradeType_id,
                newspaper_id, country_id, moderator, gradeDate,
                image_link, original_language,
                translated_article, translated_title
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            a["id"], a["title"], a["body"], a["link"], a["pubDate"],
            a["gradeType_id"], a["newspaper_id"], a["country_id"],
            a["moderator"], a["gradeDate"], a["image_link"],
            a["original_language"], a["translated_article"], a["translated_title"]
        ))

def insert_article_tags(cursor, articles: list[dict], tag_map: dict):
    for article in articles:
        article_id = article["id"]
        for tag_name in article.get("tags", []):
            tag_id = tag_map.get(tag_name)
            if not tag_id:
                print(f"[articleTags] Tag '{tag_name}' non trouvé pour article {article_id}")
                continue
            cursor.execute("""
                INSERT INTO articleTags (article_id, tag_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE tag_id = VALUES(tag_id)
            """, (article_id, tag_id))








