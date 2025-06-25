from typing import Optional
import uuid
from urllib.parse import urlparse
from langdetect import detect, LangDetectException
import re

def parse_yes_no(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    value = value.strip().lower()
    if value == "yes":
        return True
    if value == "no":
        return False
    return None

import re

TAG_VARIANTS = {
    "Society": ["Society"],
    "Geopolitics": ["Geopolitics", "Geo_politics"],
    "Politics": ["Politics"],
    "Environment": ["Environment"],
    "Business": ["Business", "Economy"],
    "Culture": ["Culture"],
    "Science": ["Science"],
    "TechScience": ["Tech", "TechScience"]
}

def extract_tags_from_string(raw_tags: str) -> list[str]:
    if not raw_tags or not isinstance(raw_tags, str):
        return []

    matched_tags = set()
    lowered = raw_tags.lower()

    for canonical_tag, variants in TAG_VARIANTS.items():
        for v in variants:
            # regex avec \b pour ne pas matcher 'Politics' dans 'Geopolitics'
            if re.search(rf"\b{re.escape(v.lower())}\b", lowered):
                matched_tags.add(canonical_tag)
                break

    return list(matched_tags)


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def extract_hostname(url: Optional[str]) -> str:
    """Extrait le hostname brut sans www d'une URL"""
    if not url:
        return ""
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    if hostname.startswith("www1."):
        hostname = hostname[5:]
    elif hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname

def get_or_create_other_newspaper(country_name, country_id, newspaper_map, cursor):
    key = f"other_{country_name.lower()}"
    if key in newspaper_map:
        return newspaper_map[key]

    newspaper_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO newspapers (id, name, link, country_id) VALUES (%s, %s, %s, %s)",
        (newspaper_id, key, None, country_id)
    )
    newspaper_map[key] = newspaper_id
    return newspaper_id

def extract_first_image_src(html: str) -> Optional[str]:
    """Extrait le premier lien d'image <img src="..."> dans une chaîne HTML"""
    if not html:
        return None
    match = re.search(r'<img\s+[^>]*src="([^"]+)"', html)
    return match.group(1) if match else None