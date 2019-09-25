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
    frontend_url VARCHAR(256),
    reporter_full_name VARCHAR(256),
    PRIMARY KEY (case_id)
)

CREATE TABLE Citations (
    case_id VARCHAR(256),
    cite VARCHAR(256),
    type VARCHAR(256),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Casebody (
    case_id VARCHAR(256),
    court VARCHAR(256),
    citation VARCHAR(256),
    decisiondate DATE,
    docket_number VARCHAR(256),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Opinions (
    author VARCHAR(256),
    opinion TEXT,
    opinion_type VARCHAR(256),
    footnote TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Parties (
    parties_id VARCHAR(256),
    case_id VARCHAR(256),
    client_A VARCHAR(256),
    client_B VARCHAR(256),
    PRIMARY KEY (parties_id),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Courts (
    court_id VARCHAR(256),
    case_id VARCHAR(256),
    jurisdiction_url VARCHAR(256),
    name VARCHAR(256),
    name_abbreviation VARCHAR(256),
    slug VARCHAR(256),
    PRIMARY KEY (court_id),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Jurisdiction (
    jurisdiction_id VARCHAR(256),
    case_id VARCHAR(256),
    name VARCHAR(256),
    name_long VARCHAR(256),
    slug VARCHAR(256),
    whitelisted BOOLEAN
    PRIMARY KEY (jurisdiction_id),
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Attorneys (
    attorney_id VARCHAR(256),
    attorneys VARCHAR(256),
    PRIMARY KEY (attorney_id)
)

CREATE TABLE Attorneys_Of (
    attorneys_id VARCHAR(256),
    case_id VARCHAR(256),
    FOREIGN KEY (attorney_id)
        REFERENCES Attorneys
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Judges (
    judges_id VARCHAR(256),
    judges VARCHAR(256),
    PRIMARY KEY (judge_id)
)

CREATE TABLE Judges_Of (
    judges_id VARCHAR(256),
    case_id VARCHAR(256),
    FOREIGN KEY (judge_id)
        REFERENCES Judges
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Headnotes (
    case_id VARCHAR(256),
    headnotes TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)

CREATE TABLE Summaries (
    case_id VARCHAR(256),
    summaries TEXT,
    FOREIGN KEY (case_id)
        REFERENCES Cases
            ON DELETE CASCADE
            ON UPDATE SET DEFAULT
)
