from typing import Optional
import uuid
from urllib.parse import urlparse
from langdetect import detect, LangDetectException
import re

def parse_yes_no(value: Optional[str]) -> Optional[bool]:
    """Parse a 'yes'/'no' string to a boolean value."""
    if value is None:
        return None
    value = value.strip().lower()
    if value == "yes":
        return True
    if value == "no":
        return False
    return None

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
    """Extract canonical tags from a raw string using defined variants."""
    if not raw_tags or not isinstance(raw_tags, str):
        return []

    matched_tags = set()
    lowered = raw_tags.lower()

    for canonical_tag, variants in TAG_VARIANTS.items():
        for v in variants:
            # Use word boundaries to avoid partial matches (e.g., avoid matching 'Politics' inside 'Geopolitics')
            if re.search(rf"\b{re.escape(v.lower())}\b", lowered):
                matched_tags.add(canonical_tag)
                break

    return list(matched_tags)

def detect_language(text: str) -> str:
    """Detect the language of a given text. Returns 'unknown' on failure."""
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def extract_hostname(url: Optional[str]) -> str:
    """Extract raw hostname without www or www1 prefix from a URL."""
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
    """Insert a fallback 'other_[country]' newspaper entry if not already present in the map."""
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
    """Extract the first <img src="..."> link from an HTML string."""
    if not html:
        return None
    match = re.search(r'<img\s+[^>]*src="([^"]+)"', html)
    return match.group(1) if match else None
