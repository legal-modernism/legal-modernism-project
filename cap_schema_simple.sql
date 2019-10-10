-- INSIDE JSON FILE
CREATE TABLE Cases (
    case_id VARCHAR(256),
    name VARCHAR(256),
    name_abbreviation VARCHAR(256)
    decision_date DATE,
    docket_number VARCHAR(256),
    first_page INTEGER,
    last_page INTEGER,
    frontend_url VARCHAR(256),
    volume_number INTEGER,
    reporter_full_name VARCHAR(256),
    PRIMARY KEY (case_id)
)
-- INSIDE JSON FILE
CREATE TABLE Citations (
    case_id VARCHAR(256),
    cite VARCHAR(256),
    type VARCHAR(256),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)
-- INSIDE JSON FILE
CREATE TABLE Courts (
    case_id VARCHAR(256),
    court_id VARCHAR(256),
    jurisdiction_url VARCHAR(256),
    name VARCHAR(256),
    name_abbreviation VARCHAR(256),
    slug VARCHAR(256),
    PRIMARY KEY (case_id, court_id),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)
-- INSIDE JSON FILE
CREATE TABLE Jurisdiction (
    case_id VARCHAR(256),
    jurisdiction_id VARCHAR(256),
    name VARCHAR(256),
    name_long VARCHAR(256),
    slug VARCHAR(256),
    whitelisted BOOLEAN,
    PRIMARY KEY (jurisdiction_id),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)
-- INSIDE XML TREE
CREATE TABLE Casebody (
    case_id VARCHAR(256),
    court VARCHAR(256),
    citation VARCHAR(256),
    decisiondate DATE,
    docket_number VARCHAR(256),
    judges VARCHAR(256), -- Judge TABLE
    parties VARCHAR(256), -- PARTIES TABLE
    headnotes TEXT, -- HEADNOTES TABLE
    summaries TEXT, -- SUMMARIEIS
    opinions TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)
-- INSIDE XML TREE
CREATE TABLE Attorneys_Of (
    attorneys VARCHAR(256),
    case_id VARCHAR(256),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)
