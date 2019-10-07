# case-law-access-project

This repository stores the codebase for the case law access project

## Directory
    .
    ├── data                    # Subfolder to store data from CAP api
    ├── code                    # Github source code here
    │   ├── main.py
    │   ├── cap_postgresql.py
    │   ├── cap_api.py
    │   ├── utility.py
    └── └── README.md

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

To run this locally, create a database.ini file to access postgresql
```bash
touch database.ini
```

Copy/paste this, fill in details

```
[postgresql]
host=
database=
user=
password=
```

Run main.py
```python
python main.py
```

## Source
https://case.law
