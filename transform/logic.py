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
    # Remove embedded articles from the record if present
    record.pop("articles", None)

    country_name = record.get("country")
    country_id = country_map.get(country_name)

    if not country_id:
        print(f"[WARNING] Country '{country_name}' not found in country_map")
        return None

    record["country_id"] = country_id
    record.pop("country", None)

    record["id"] = record.get("newspaper_id")
    record.pop("newspaper_id", None)

    record["name"] = record.get("newspaper_name")
    record.pop("newspaper_name", None)
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
                id=get_country_code(country),
                name=country,
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
            print(f"[country] Transformation error: {e}")
    return result


def transform_article_record(
    record: dict,
    grade_type_table: dict,
    country_map: dict,
    newspaper_map: dict,
    tag_list_enabled: bool,
    db_cursor,
) -> Optional[dict]:
    try:
        # Article body
        body = record.get("contentSnippet") or None
        original_language = detect_language(body) if body else None

        # Dates
        pub_date = record.get("pubDate")
        grade_date = record.get("gradeDate")

        # Grade type
        grade_type_name = record.get("type", "ungraded").lower()
        print(grade_type_name)
        grade_type_id = grade_type_table.get(grade_type_name)

        # Newspaper
        link = record.get("link", "")
        hostname = extract_hostname(link)
        newspaper_id = newspaper_map.get(hostname)

        # Country logic fallback
        if newspaper_id:
            # Retrieve country from DB if newspaper is found
            db_cursor.execute("SELECT country_id FROM newspapers WHERE id = %s", (newspaper_id,))
            result = db_cursor.fetchone()
            country_id = result["country_id"] if result else None
        else:
            # Attempt to map country from raw name
            country_name = (record.get("country") or "").strip()
            country_id = country_map.get(country_name)

            if not newspaper_id:
                if not country_id:
                    print(f"[article] No country_id available, fallback not possible for link={link}")
                    return None
                # Create 'other_[country]' newspaper entry
                newspaper_id = get_or_create_other_newspaper(
                    country_name, country_id, newspaper_map, db_cursor
                )

        # Image extraction
        content_html = record.get("content") or ""
        image_link = extract_first_image_src(content_html)

        # Tags
        raw_tags = record.get("tags", "")
        tags = extract_tags_from_string(raw_tags) if tag_list_enabled else []

        # Future gradeDate handling
        moderator = record.get("moderator")
        if grade_date and isinstance(grade_date, datetime) and grade_date.date() > datetime(2024, 6, 30).date():
            grade_type_id = grade_type_table.get("ungraded")
            moderator = None
            tags = []
            grade_date = None

        # Title truncation
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
            moderator=moderator,
            gradeDate=grade_date,
            image_link=image_link,
            original_language=original_language,
            translated_article=None,
            translated_title=None,
            tags=tags,
        )

        return article.model_dump()

    except Exception as e:
        print(f"[article] Transformation error: {e}")
        return None
