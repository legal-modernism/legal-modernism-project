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
    case_id VARCHAR(255),
    name VARCHAR(255),
    name_abbreviation VARCHAR(255),
    decision_date DATE,
    docket_number VARCHAR(255),
    first_page INTEGER,
    last_page INTEGER,
    frontend_url VARCHAR(255),
    volume_number INTEGER,
    reporter_full_name VARCHAR(255),
    PRIMARY KEY (case_id)
);

CREATE TABLE Citations (
    case_id VARCHAR(255),
    cite VARCHAR(255),
    type VARCHAR(255),
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Jurisdiction (
    jurisdiction_id VARCHAR(255),
    case_id VARCHAR(255),
    name VARCHAR(255),
    name_long VARCHAR(255),
    slug VARCHAR(255),
    whitelisted BOOLEAN,
    PRIMARY KEY (jurisdiction_id),
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Courts (
    case_id VARCHAR(255),
    court_id VARCHAR(255),
    jurisdiction_url VARCHAR(255),
    name VARCHAR(255),
    name_abbreviation VARCHAR(255),
    slug VARCHAR(255),
    PRIMARY KEY (court_id),
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Parties (
    case_id VARCHAR(255),
    parties_id VARCHAR(255),
    parties VARCHAR(255),
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Judges (
    case_id VARCHAR(255),
    judges_id VARCHAR(255),
    judges VARCHAR(255),
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Attorneys (
    case_id VARCHAR(255),
    attorneys_id VARCHAR(255),
    attorneys VARCHAR(255),
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Headnotes (
    case_id VARCHAR(255),
    headnotes_id VARCHAR(255),
    headnotes TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Summary (
    case_id VARCHAR(255),
    summary_id VARCHAR(255),
    summary TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
);

CREATE TABLE Opinion (
    case_id VARCHAR(255),
    opinion_type VARCHAR(255),
    text_type VARCHAR(255),
    text_id VARCHAR(255),
    text TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
);
