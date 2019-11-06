CREATE TABLE Cases (
    case_id VARCHAR(256),
    name VARCHAR(256),
    name_abbreviation VARCHAR(256),
    decision_date DATE,
    docket_number VARCHAR(256),
    first_page INTEGER,
    last_page INTEGER,
    frontend_url VARCHAR(256),
    volume_number INTEGER,
    reporter_full_name VARCHAR(256),
    PRIMARY KEY (case_id)
);

CREATE TABLE Citations (
    case_id VARCHAR(256),
    cite VARCHAR(256),
    type VARCHAR(256),
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Jurisdiction (
    jurisdiction_id VARCHAR(256),
    case_id VARCHAR(256),
    name VARCHAR(256),
    name_long VARCHAR(256),
    slug VARCHAR(256),
    whitelisted BOOLEAN,
    PRIMARY KEY (jurisdiction_id),
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Courts (
    case_id VARCHAR(256),
    court_id VARCHAR(256),
    jurisdiction_url VARCHAR(256),
    name VARCHAR(256),
    name_abbreviation VARCHAR(256),
    slug VARCHAR(256),
    PRIMARY KEY (court_id),
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Parties (
    case_id VARCHAR(256),
    parties VARCHAR(256),
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Judges (
    case_id VARCHAR(256),
    judges VARCHAR(256),
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Attorneys (
    case_id VARCHAR(256),
    attorneys VARCHAR(256),
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Headnotes (
    case_id VARCHAR(256),
    headnotes TEXT,
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Summaries (
    case_id VARCHAR(256),
    summaries TEXT,
    FOREIGN KEY (case_id)
      REFERENCES Cases
);

CREATE TABLE Opinions (
    case_id VARCHAR(256),
    author VARCHAR(256),
    opinion TEXT,
    opinion_type VARCHAR(256),
    footnote TEXT,
    FOREIGN KEY (case_id)
      REFERENCES Cases
);
