import uuid
from models.schemas import Newspaper, CountryClean, ArticleClean
from utils.helpers import (
    extract_tags_from_string,
    detect_language,
    extract_hostname,
    parse_yes_no,
    get_or_create_other_newspaper,
    extract_first_image_src,
)
from typing import Optional
from mysql.connector.cursor import MySQLCursor
from utils.iso import get_country_code
from datetime import datetime


def transform_newspaper_record(record: dict, country_map: dict) -> dict:
    record.pop("articles", None)

    country_name = record.get("country")
    country_id = country_map.get(country_name)

    if not country_id:
        print(f"[WARNING] Country '{country_name}' not found in country_map")
        return None

    record["country_id"] = country_id
    record.pop("country", None)

    return record
    

def transform_country_records(rows: list[dict]) -> list[dict]:
    seen = {}
    for row in rows:
        key = row["countryName"]
        if key not in seen:
            seen[key] = row

    result = []
    for country, data in seen.items():
        try:
            clean = CountryClean(
                country_id=get_country_code(country),
                country=country,
                flag_logo=data.get("flagLogo"),
                unsc=parse_yes_no(data.get("unsc")),
                qsd=parse_yes_no(data.get("qsd")),
                five_eyes=parse_yes_no(data.get("fiveEyes")),
                eco_rank=data.get("ecoRank"),
                diasporic_rank=data.get("diaspRank"),
                border_dispute=parse_yes_no(data.get("borDisp")),
                brics=parse_yes_no(data.get("brics")),
                import_rank=data.get("importRank"),
                export_rank=data.get("exportRank"),
                defense_rank=data.get("defenseRank"),
                tourism_rank=data.get("tourismRank"),
                nuclear=parse_yes_no(data.get("nuclear"))
            )
            result.append(clean.model_dump())
        except Exception as e:
            print(f"[country] Erreur transformation: {e}")
    return result


# Correspondance gradeType brute → canonique
GRADE_TYPE_MAP = {
    "positive": "Positive",
    "negative": "Negative",
    "neutral": "Neutral",
    "irrelevant": "Irrelevant",
    "ungraded": "Ungraded"
}

def transform_article_record(
    record: dict,
    grade_type_table: dict,
    country_map: dict,
    newspaper_map: dict,
    tag_list_enabled: bool,
    db_cursor,
) -> Optional[dict]:
    try:
        # 💬 Corps de l'article
        body = record.get("contentSnippet") or None
        original_language = detect_language(body) if body else None

        # 🕒 Dates
        pub_date = record.get("pubDate")
        grade_date = record.get("gradeDate")

        # 🏷️ Type de note
        raw_type = (record.get("type") or "").strip().lower()
        grade_type_name = GRADE_TYPE_MAP.get(raw_type, "Ungraded")
        grade_type_id = grade_type_table.get(grade_type_name)

        # 🗞️ Journal
        link = record.get("link", "")
        hostname = extract_hostname(link)
        newspaper_id = newspaper_map.get(hostname)

        # 🌍 Pays (correction de la logique)
        if newspaper_id:
            # Si journal trouvé, on récupère le pays depuis la DB
            db_cursor.execute("SELECT country_id FROM newspapers WHERE newspaper_id = %s", (newspaper_id,))
            result = db_cursor.fetchone()
            country_id = result["country_id"] if result else None
        else:
            # Sinon, on essaie de mapper à partir du nom de pays brut
            country_name = (record.get("country") or "").strip()
            country_id = country_map.get(country_name)

            if not newspaper_id:
                if not country_id:
                    print(f"[article] Pas de country_id → pas de fallback possible pour link={link}")
                    return None
                # 🆕 Création de 'other_[country]'
                newspaper_id = get_or_create_other_newspaper(
                    country_name, country_id, newspaper_map, db_cursor
                )

        # 🖼️ Image
        content_html = record.get("content") or ""
        image_link = extract_first_image_src(content_html)

        # 🏷️ Tags
        raw_tags = record.get("tags", "")
        tags = extract_tags_from_string(raw_tags) if tag_list_enabled else []
        

        # 🛑 Règle spéciale : gradeDate future
        moderator = record.get("moderator")
        if grade_date and isinstance(grade_date, datetime) and grade_date.date() > datetime(2024, 6, 30).date():
            grade_type_id = grade_type_table.get("Ungraded")
            moderator = None
            tags = []
            grade_date = None
        # 📝 Titre
        raw_title = record.get("title", "")
        title = raw_title[:500] + "..." if len(raw_title) > 512 else raw_title
        article = ArticleClean(
            id=str(uuid.uuid4()),
            title=title,
            body=body,
            link=link,
            pubDate=pub_date,
            gradeType_id=grade_type_id,
            newspaper_id=newspaper_id,
            country_id=country_id,
            moderator=record.get("moderator"),
            gradeDate=grade_date,
            image_link=image_link,
            original_language=original_language,
            translated_article=None,
            translated_title=None,
            tags=tags,
        )

        return article.model_dump()

    except Exception as e:
        print(f"[article] Erreur transformation : {e}")
        return None