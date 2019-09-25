# case-law-access-project

This repository stores the codebase for the case law access project

## Installation

Create a virtual environment
```bash
virtualenv venv
source venv/bin/activate
```

Install requirements via pip
```bash
pip install -r requirements.txt
```

## Usage

Store the API_Key in .env file. Don't share this with others.

```bash
echo 'export API_KEY="insert_your_key_here"' > .env
```

Create a database.ini file to access postgresql
```
touch database.ini
```

Copy/paste this, fill in details

[postgresql]
host=
database=
user=
password=

To download the files:
```python
python main.py
```

To access PostgreSQL database:
```python
python postresql_database.py
```


## Source
https://case.law
