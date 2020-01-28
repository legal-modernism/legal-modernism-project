DROP TABLE IF EXISTS Legal_Treatises_Metadata CASCADE;
DROP TABLE IF EXISTS Book_Info CASCADE;
DROP TABLE IF EXISTS Book_Citation CASCADE;
DROP TABLE IF EXISTS Book_Subject CASCADE;
DROP TABLE IF EXISTS Book_volumeSet CASCADE;
DROP TABLE IF EXISTS Book_locSubjectHead CASCADE;
DROP TABLE IF EXISTS Page CASCADE;
DROP TABLE IF EXISTS Page_Content CASCADE;
DROP TABLE IF EXISTS Page_ocrText CASCADE;

CREATE TABLE Legal_Treatises_Metadata (
    PSMID VARCHAR(255),
    author_by_line TEXT, -- VARCHAR(255)
    title TEXT,
    edition TEXT, -- VARCHAR(255)
    current_volume VARCHAR(255), -- INTEGER
    imprint VARCHAR(255),
    book_collation VARCHAR(255),
    pages VARCHAR(255), -- INTEGER
    PRIMARY KEY (PSMID)
);

CREATE TABLE Book_Info (
    PSMID VARCHAR(255),
    contentType VARCHAR(255),
    ID VARCHAR(255),
    FAID VARCHAR(255),
    COLID VARCHAR(255),
    ocr VARCHAR(255),
    assetID VARCHAR(255),
    assetIDeTOC VARCHAR(255),
    dviCollectionID VARCHAR(255),
    bibliographicID VARCHAR(255),
    bibliographicID_type VARCHAR(255),
    unit VARCHAR(255), -- INTEGER
    ficheRange VARCHAR(255),
    mcode VARCHAR(255),
    pubDate_year VARCHAR(255), -- DATE
    pubDate_composed VARCHAR(255), -- DATE
    pubDate_pubDateStart VARCHAR(255), -- INTEGER
    releaseDate VARCHAR(255), -- INTEGER
    sourceLibrary_libraryName VARCHAR(255),
    sourceLibrary_libraryLocation VARCHAR(255),
    language VARCHAR(255),
    language_ocr VARCHAR(255),
    language_primary VARCHAR(255),
    documentType VARCHAR(255),
    notes VARCHAR(255),
    categoryCode VARCHAR(255),
    categoryCode_source VARCHAR(255),
    ProductLink TEXT,
    PRIMARY KEY (PSMID)
);

CREATE TABLE Book_Citation (
    PSMID VARCHAR(255),
    author_role VARCHAR(255),
    author_composed VARCHAR(255),
    author_first VARCHAR(255),
    author_middle VARCHAR(255),
    author_last VARCHAR(255),
    author_birthDate VARCHAR(255), -- DATE
    author_deathDate VARCHAR(255), -- DATE
    fullTitle TEXT,
    displayTitle TEXT,
    variantTitle TEXT,
    edition VARCHAR(255), -- INTEGER
    editionStatement VARCHAR(255),
    currentVolume VARCHAR(255), -- INTEGER
    volume VARCHAR(255), -- INTEGER
    totalVolume VARCHAR(255), -- INTEGER
    imprintFull VARCHAR(255),
    imprintPublisher VARCHAR(255),
    book_collation VARCHAR(255),
    publicationPlaceCity VARCHAR(255),
    publicationPlaceComposed VARCHAR(255),
    totalPages VARCHAR(255), -- INTEGER
    FOREIGN KEY (PSMID)
        REFERENCES Book_Info (PSMID)
);

CREATE TABLE Book_Subject (
    PSMID VARCHAR(255),
    subject VARCHAR(255),
    source VARCHAR(255),
    FOREIGN KEY (PSMID)
        REFERENCES Book_Info (PSMID)
);

CREATE TABLE Book_volumeSet (
    PSMID VARCHAR(255),
    volumeID VARCHAR(255),
    assetID VARCHAR(255),
    filmedVolume VARCHAR(255),
    FOREIGN KEY (PSMID)
        REFERENCES Book_Info (PSMID)
);

CREATE TABLE Book_locSubjectHead (
    PSMID VARCHAR(255),
    type VARCHAR(255),
    subField VARCHAR(255),
    locSubject VARCHAR(255),
    FOREIGN KEY (PSMID)
        REFERENCES Book_Info (PSMID)
);

CREATE TABLE Page (
    pageID VARCHAR(255),
    PSMID VARCHAR(255),
    type VARCHAR(255),
    firstPage VARCHAR(255),
    assetID VARCHAR(255),
    ocrLanguage VARCHAR(255),
    sourcePage VARCHAR(255), -- INTEGER
    ocr VARCHAR(255),
    imageLink_pageIndicator VARCHAR(255),
    imageLink_width VARCHAR(255), -- INTEGER
    imageLink_height VARCHAR(255), -- INTEGER
    imageLink_type VARCHAR(255),
    imageLink_colorimage VARCHAR(255),
    imageLink VARCHAR(255),
    PRIMARY KEY (pageID, PSMID),
    FOREIGN KEY (PSMID)
        REFERENCES Book_Info (PSMID)
);


-- THERE IS A PROBLEM HERE
CREATE TABLE Page_Content (
    pageID VARCHAR(255),
    PSMID VARCHAR(255),
    sectionHeader_type VARCHAR(255),
    sectionHeader VARCHAR(255),
    FOREIGN KEY (pageID, PSMID)
        REFERENCES Page (pageID, PSMID)--,
    -- FOREIGN KEY (PSMID)
    --    REFERENCES Book_Info (PSMID)
);

CREATE TABLE Page_ocrText (
    pageID VARCHAR(255),
    PSMID VARCHAR(255),
    ocrText TEXT,
    FOREIGN KEY (pageID, PSMID)
        REFERENCES Page (pageID, PSMID)--,
    -- FOREIGN KEY (PSMID)
    --     REFERENCES Book_Info (PSMID)
);
