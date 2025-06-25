def create_newspapers_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS newspapers (
            id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            link VARCHAR(255),
            country_id CHAR(2) NOT NULL, -- Foreign key to countries table
            monthly_readers INT,
            political_inclination VARCHAR(255),
            basic_info TEXT,
            logo TEXT,
            owner VARCHAR(255),
            FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
        )
    """)



def create_countries_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id CHAR(2) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            flag_logo VARCHAR(255),
            unsc BOOLEAN,
            qsd BOOLEAN,
            five_eyes BOOLEAN,
            eco_rank INT,
            diasporic_rank INT,
            border_dispute BOOLEAN,
            brics BOOLEAN,
            import_rank INT,
            export_rank INT,
            defense_rank INT,
            tourism_rank INT,
            nuclear BOOLEAN
        )
    """)

def create_grade_types_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gradeTypes (
            id CHAR(36) PRIMARY KEY,
            type VARCHAR(255) UNIQUE NOT NULL
        )
    """)

def create_tags_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        )
    """)

def create_articles_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id CHAR(36) PRIMARY KEY,
            title VARCHAR(512) NOT NULL,
            body TEXT,
            link TEXT NOT NULL,
            pubDate DATETIME NOT NULL,
            gradeType_id CHAR(36) NOT NULL,
            newspaper_id CHAR(36) NOT NULL,
            country_id CHAR(2) NOT NULL,
            moderator VARCHAR(255),
            gradeDate DATE,
            image_link TEXT,
            original_language VARCHAR(50),
            translated_article TEXT,
            translated_title VARCHAR(255),
            FOREIGN KEY (gradeType_id) REFERENCES gradeTypes(id),
            FOREIGN KEY (newspaper_id) REFERENCES newspapers(id),
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    """)

def create_article_tags_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articleTags (
            article_id CHAR(36) NOT NULL,
            tag_id CHAR(36) NOT NULL,
            PRIMARY KEY (article_id, tag_id),
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        )
    """)