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
('bd-news-0001-0000-0000-000000000001', 'banglatribune.com', 'https://www.banglatribune.com/', 'Bangladesh', 3000000, 'Neutral; focuses on accurate and timely news', 'Online news platform; delivers news in Bengali; focuses on accuracy and speed; popular among digital news consumers. ', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRj_NwtQJakgNbWXIc9PrZQYpZyzqfRJ6XE7A&s', NULL, 'Bangla Tribune Media Limited'),

-- weeklyblitz.net
('bd-news-0002-0000-0000-000000000002', 'dhakapost.com', 'https://www.dhakapost.com/', 'Bangladesh', 2000000, 'Emerging; aims for balanced reporting.', 'Emerging online news portal; provides up-to-date news on various topics; caters to a broad audience.', 'https://upload.wikimedia.org/wikipedia/commons/5/56/Dhaka_post.jpg', NULL, "Dhaka Post Media Group, it is a newer addition to Bangladesh's media"),

-- tv9bangla.com
('bd-news-0003-0000-0000-000000000003', 'bd-pratidin.com', 'https://www.bd-pratidin.com/', 'Bangladesh', 8000000, 'Neutral; widely circulated; general news coverage.', 'One of the highest-circulated Bengali dailies; offers diverse news content; accessible online for free', 'https://play-lh.googleusercontent.com/FazQLOWAQy6DrG7xpC_DJ2nYm-HnU-NJJeiG6ggO8hSzgT-L5M8bR8EQK2w2ETFz6Ts', NULL, 'East West Media Group, which is part of the Bashundhara Group'),

-- freelancer.com.bd
('bd-news-0004-0000-0000-000000000004', 'kalerkantho.com', 'https://www.kalerkantho.com/', 'Bangladesh', 10000000, 'Neutral; covers a broad spectrum of news', 'Launched in 2010; Bengali-language daily; rapidly gained readership; known for comprehensive news coverage. ', 'https://logovectordl.com/wp-content/uploads/2019/12/kaler-kantho-logo-vector.png', NULL, 'East West Media Group, a part of the Bashundhara Group'),

-- flickr.com
('bd-news-0005-0000-0000-000000000005', 'thedailystar.net', 'https://www.thedailystar.net/', 'Bangladesh', 5000000, 'Independent; focuses on objective reporting.', 'Founded in 1991; prominent English-language daily; covers national and international news; widely read by policymakers and the international community.', 'https://images.seeklogo.com/logo-png/35/1/the-daily-star-logo-png_seeklogo-351053.png?v=1957294212613335576', NULL, 'Mediaworld Limited(Transcom) '),

-- benarnews.org
('bd-news-0006-0000-0000-000000000006', 'prothomalo.com', 'https://www.prothomalo.com/', 'Bangladesh', 25000000, 'Independent; emphasizes journalistic integrity', 'Established in 1998; leading Bengali-language daily; significant online presence; over 6.6 million daily readers online', 'https://images.prothomalo.com/prothomalo/import/default/2016/03/15/4d3620a7127d4a031a05a962fcc4b253-palo-logo.jpg', NULL, 'Transcom Group');




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
-- okaz.com.sa
('sa-news-0003-0000-0000-000000000001', 'okaz.com.sa', 'https://www.okaz.com.sa/', 'Saudi Arabia', 3300000, 'Liberal-leaning but pro-establishment', 'Major Arabic daily, tabloid style, HQ Jeddah (1960)', 'https://iconape.com/wp-content/files/cl/8520/png/Okaz-01.png', NULL, 'Okaz Org. for Press & Publication; founded by Ahmad Attar (1960) (en.wikipedia.org)'),

-- al jarizah
('sa-news-0001-0000-0000-000000000002', 'aljazeera.com', 'https://www.aljazeera.com/', 'Saudi Arabia', NULL, 'Pro-government', 'Daily since 1964, Riyadh-based tabloid', 'https://www.seekpng.com/png/detail/406-4064747_al-jazeera-logo-png.png', NULL, 'Al Jazirah Corp. for Press, Printing & Publishing (1960)'),

-- al wantan
('sa-news-0002-0000-0000-000000000003', 'alwatannews.net', 'https://alwatannews.net/', 'Saudi Arabia', 2700000, 'Pro-government', 'Regional daily since 2000', 'https://alwatannews.net/theme_watanbahrain/images/fb_image.jpg', NULL, 'Founded by Saudi royals; est. 2000 in Abha (Tehran article earlier conflated w/ Qatar)'),

-- aawsat
('sa-news-0001-0000-0000-000000000004', 'aawsat.com', 'https://aawsat.com/', 'Saudi Arabia', 8000000, 'Pro-Saudi government', 'International Arabic daily based in London', 'https://english.aawsat.com/themes/custom/enaawsatv3/img/sharelogoimage.jpg', NULL, 'Saudi Research & Media Group; royal family ownership (1978)'),

-- arabnews.com
('sa-news-0002-0000-0000-000000000005', 'arabnews.com', 'https://www.arabnews.com/', 'Saudi Arabia', 2200000, 'Centrist, pro-establishment', 'English daily founded 1975', 'https://www.arabnews.com/sites/all/themes/narabnews/assets/img/logo-with-banners.png?22', NULL, 'TBN & SRMG (English sister to Okaz)'),

-- saudigazette.com.sa
('sa-news-0001-0000-0000-000000000006', 'saudigazette.com.sa', 'https://saudigazette.com.sa/', 'Saudi Arabia', 690000, 'Pro-government (editorial constraints)', 'English daily launched 1976', 'https://saudigazette.com.sa/themes/saudigazette/images/SG-logo.svg', NULL, 'Okaz Organization; English-language sister of Okaz'),

-- al madina
('sa-news-0002-0000-0000-000000000007', 'al-madina.com', 'https://al-madina.com/', 'Saudi Arabia', 280000, 'Pro-government', 'Local Jeddah daily covering regional affairs', 'https://al-madina.com/theme_madina/images/main-logo.png', NULL, 'Owned by state-linked entity');


UPDATE countryCounts
SET
    brics = "No",
    ecoRank = 3
WHERE countryName = 'Germany';

UPDATE countryCounts
SET
    brics = "No",
    ecoRank = 4
WHERE countryName = 'Japan';

UPDATE countryCounts
SET
    brics = "Yes"
WHERE countryName = 'Canada';