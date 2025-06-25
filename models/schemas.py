from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class Newspaper(BaseModel):
    id: str
    name: str
    link: Optional[str] = None
    country_id: str
    monthly_readers: Optional[int] = None
    political_inclination: Optional[str] = None
    basic_info: Optional[str] = None
    logo: Optional[str] = None
    owner: Optional[str] = None



class CountryClean(BaseModel):
    id: str
    name: str
    flag_logo: Optional[str]
    unsc: Optional[bool]
    qsd: Optional[bool]
    five_eyes: Optional[bool]
    eco_rank: Optional[int]
    diasporic_rank: Optional[int]
    border_dispute: Optional[bool]
    brics: Optional[bool]
    import_rank: Optional[int]
    export_rank: Optional[int]
    defense_rank: Optional[int]
    tourism_rank: Optional[int]
    nuclear: Optional[bool]

class ArticleClean(BaseModel):
    id: str
    title: str
    body: Optional[str]
    link: str
    pubDate: datetime
    gradeType_id: str
    newspaper_id: str
    country_id: str
    moderator: Optional[str]
    gradeDate: Optional[date]
    image_link: Optional[str]
    original_language: Optional[str]
    translated_article: Optional[str]
    translated_title: Optional[str]
    tags: List[str]  # noms des tags, à relier ensuite


class GradeType(BaseModel):
    id: str
    type: str


class Tag(BaseModel):
    id: str
    name: str