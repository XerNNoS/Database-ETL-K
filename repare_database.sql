UPDATE newspapers
SET 
    logo = link,
    link = 'https://www.courrierinternational.com/'
WHERE newspaper_name = 'courrierinternational.com';



DELETE FROM countryCounts
WHERE countryName = 'South Africa'
  AND ecoRank != 37;


INSERT INTO countryCounts (
    flag_id,
    countryName,
    type,
    flagLogo,
    Articles,
    unsc,
    qsd,
    fiveEyes,
    ecoRank,
    diaspRank,
    borDisp,
    brics,
    importRank,
    exportRank,
    defenseRank,
    tourismRank,
    nuclear
)
VALUES (
    'bd123456-7890-4abc-def0-1234567890bd', -- flag_id: fake UUID
    'Bangladesh',                           -- countryName
    'Neutral',                              -- type
    NULL,                                   -- flagLogo (nullable)
    999999,                                 -- Articles (int, NOT NULL)
    'No',                                   -- unsc (varchar, NOT NULL)
    'N/A',                                  -- qsd
    'No',                                   -- fiveEyes
    35,                                     -- ecoRank (int, NOT NULL)
    -1,                                     -- diaspRank
    'None',                                 -- borDisp
    'No',                                   -- brics
    34,                                     -- importRank
    8,                                      -- exportRank
    -1,                                     -- defenseRank
    1,                                      -- tourismRank
    'No'                                    -- nuclear (nullable)
);


INSERT INTO newspapers (
    newspaper_id,
    newspaper_name,
    link,
    country,
    monthly_readers,
    political_inclination,
    basic_info,
    logo,
    articles,
    owner
) VALUES
-- bangladeshsun.com
('bd-news-0001-0000-0000-000000000001', 'bangladeshsun.com', 'https://www.bangladeshsun.com/', 'Bangladesh', NULL, NULL, NULL, NULL, NULL, NULL),

-- weeklyblitz.net
('bd-news-0002-0000-0000-000000000002', 'weeklyblitz.net', 'https://weeklyblitz.net/', 'Bangladesh', NULL, NULL, NULL, NULL, NULL, NULL),

-- tv9bangla.com
('bd-news-0003-0000-0000-000000000003', 'tv9bangla.com', 'https://tv9bangla.com/', 'Bangladesh', NULL, NULL, NULL, NULL, NULL, NULL),

-- freelancer.com.bd
('bd-news-0004-0000-0000-000000000004', 'freelancer.com.bd', 'https://www.freelancer.com.bd/', 'Bangladesh', NULL, NULL, NULL, NULL, NULL, NULL),

-- flickr.com
('bd-news-0005-0000-0000-000000000005', 'flickr.com', 'https://www.flickr.com/', 'Bangladesh', NULL, NULL, NULL, NULL, NULL, NULL),

-- benarnews.org
('bd-news-0006-0000-0000-000000000006', 'benarnews.org', 'https://www.benarnews.org/', 'Bangladesh', NULL, NULL, NULL, NULL, NULL, NULL);




UPDATE ungradedArticles
SET 
    country = 'Saudi Arabia'
WHERE country = 'Saudi';


INSERT INTO newspapers (
    newspaper_id,
    newspaper_name,
    link,
    country,
    monthly_readers,
    political_inclination,
    basic_info,
    logo,
    articles,
    owner
) VALUES
-- saudigazette.com.sa
('sa-news-0001-0000-0000-000000000001', 'saudigazette.com.sa', 'https://www.saudigazette.com.sa/', 'Saudi Arabia', NULL, NULL, NULL, NULL, NULL, NULL),

-- arabnews.com
('sa-news-0002-0000-0000-000000000002', 'arabnews.com', 'https://www.arabnews.com/', 'Saudi Arabia', NULL, NULL, NULL, NULL, NULL, NULL),

-- okaz.com.sa
('sa-news-0003-0000-0000-000000000003', 'okaz.com.sa', 'https://www.okaz.com.sa/', 'Saudi Arabia', NULL, NULL, NULL, NULL, NULL, NULL);

UPDATE countries
SET
    brics = "No",
    ecoRank = 3
WHERE countryName = 'Germany';

UPDATE countries
SET
    brics = "No",
    ecoRank = 4
WHERE countryName = 'Japan';

UPDATE countries
SET
    brics = "Yes"
WHERE countryName = 'Canada';