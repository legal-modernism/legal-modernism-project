DROP TABLE IF EXISTS Cases CASCADE;
DROP TABLE IF EXISTS Citations CASCADE;
DROP TABLE IF EXISTS Jurisdiction CASCADE;
DROP TABLE IF EXISTS Courts CASCADE;
DROP TABLE IF EXISTS Parties CASCADE;
DROP TABLE IF EXISTS Judges CASCADE;
DROP TABLE IF EXISTS Attorneys CASCADE;
DROP TABLE IF EXISTS Headnotes CASCADE;
DROP TABLE IF EXISTS Summary CASCADE;
DROP TABLE IF EXISTS Opinion CASCADE;

CREATE TABLE Cases (
    case_id VARCHAR(510),
    name TEXT, -- This MUST be a TEXT
    name_abbreviation VARCHAR(511),
    decision_date VARCHAR(510), -- Some dates are not in date form?
    docket_number VARCHAR(512),
    first_page INTEGER,
    last_page INTEGER,
    frontend_url VARCHAR(513),
    volume_number INTEGER,
    reporter_full_name VARCHAR(514),
    PRIMARY KEY (case_id)
);

CREATE TABLE Citations (
    case_id VARCHAR(515),
    cite VARCHAR(516),
    type VARCHAR(517),
    FOREIGN KEY (case_id)
        REFERENCES Cases (case_id)
);

CREATE TABLE Jurisdiction (
    jurisdiction_id VARCHAR(518),
    case_id VARCHAR(519),
    name VARCHAR(520),
    name_long VARCHAR(521),
    slug VARCHAR(522),
    whitelisted BOOLEAN,
    PRIMARY KEY (jurisdiction_id, case_id), -- Must be two
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Courts (
    case_id VARCHAR(523),
    court_id VARCHAR(524),
    jurisdiction_url VARCHAR(525),
    name VARCHAR(526),
    name_abbreviation VARCHAR(527),
    slug VARCHAR(528),
    PRIMARY KEY (court_id, case_id), -- Must be two
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Parties (
    case_id VARCHAR(529),
    parties_id VARCHAR(530),
    parties TEXT, -- this MUST be a TEXT
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Judges (
    case_id VARCHAR(532),
    judges_id VARCHAR(533),
    judges VARCHAR(534),
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Attorneys (
    case_id VARCHAR(535),
    attorneys_id VARCHAR(536),
    attorneys TEXT, -- This must be a TEXT
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Headnotes (
    case_id VARCHAR(538),
    headnotes_id VARCHAR(539),
    headnotes TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Summary (
    case_id VARCHAR(540),
    summary_id VARCHAR(541),
    summary TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Opinion (
    case_id VARCHAR(542),
    opinion_type VARCHAR(543),
    text_type VARCHAR(544),
    text_id VARCHAR(545),
    text TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
);
