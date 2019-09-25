/*
Author
Think about enforcing referential constraints later!
i.e. ON DELETE CASCADE
     ON UPDATE SET DEFAULT

etc etc .,,
*/

CREATE TABLE Cases
  (case_id VARCHAR(256),
  name VARCHAR(256),
  name_abbreviation VARCHAR(256)
  decision_date DATE,
  docket_number VARCHAR(256),
  first_page INTEGER,
  last_page INTEGER,
  frontend_url VARCHAR(256),
  volume_number INTEGER,
  frontend_url VARCHAR(256),
  PRIMARY KEY (case_id))

CREATE TABLE Casebody
  (case_id VARCHAR(256) NOT NULL,
  parties_id VARCHAR(256),
  docket_number_id VARCHAR(256)
  decisiondate DATE,
  author VARCHAR(256),
  footnote VARCHAR(256),
  footnote_label VARCHAR(256),
  opinion TEXT,
  opinion_type VARCHAR(256)
  FOREIGN KEY (case_id) REFERENCES Cases)

CREATE TABLE Courts
  (court_id VARCHAR(256),
  case_id VARCHAR(256),
  jurisdiction_url VARCHAR(256),
  name VARCHAR(256),
  name_abbreviation VARCHAR(256),
  slug VARCHAR(256),
  PRIMARY KEY (court_id),
  FOREIGN KEY (case_id) REFERENCES Cases)

CREATE TABLE Jurisdiction
  (jurisdiction_id VARCHAR(256),
  case_id VARCHAR(256),
  jurisdiction_name VARCHAR(256),
  jurisdiction_name_long VARCHAR(256),
  jurisdiction_slug VARCHAR(256),
  jurisdiction_white_listed BOOLEAN
  PRIMARY KEY (jurisdiction_id),
  FOREIGN KEY (case_id) REFERENCES Cases
)

CREATE TABLE Attorneys
  (attorney_id VARCHAR(256),
  attorney_name VARCHAR(256),
  PRIMARY KEY (attorney_id))

/*
CREATE TABLE Attorney_Of
  (attorney_id VARCHAR(256),
  case_id VARCHAR(256),
  FOREIGN KEY (attorney_id) REFERENCES Attorneys,
  FOREIGN KEY (case_id) REFERENCES Cases)
*/

CREATE TABLE Judges
  (judge_id VARCHAR(256),
  judge_name VARCHAR(256),
  PRIMARY KEY (judge_id))

/*
CREATE TABLE Judge_Of
  (judge_id VARCHAR(256),
  case_id VARCHAR(256),
  FOREIGN KEY (judge_id) REFERENCES Judges,
  FOREIGN KEY (case_id) REFERENCES Cases)
*/

CREATE TABLE Headnotes
  (case_id VARCHAR(256),
  headnotes TEXT,
  FOREIGN KEY (case_id) REFERENCES Cases)

CREATE TABLE Summaries
  (case_id VARCHAR(256),
  summaries TEXT,
  FOREIGN KEY (case_id) REFERENCES Cases)
