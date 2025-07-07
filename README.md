# SQLAlchemy Database Toolkit

**A modular toolkit for building, configuring, and managing databases using SQLAlchemy**

The SQLAlchemy Database Toolkit simplifies the setup and management across different relational databases.  
Currently, it handles configuration loading, engine creation, ORM base registration, and session management.  
It provides an extensible foundation for rapid database development, prototyping, and integration into data pipelines or applications.  

Supported DBMS under current version:
- **MySQL**
- **PostgreSQL**
- **SQLite**


## Table of Contents

- [Requirements](#requirements)
- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)


## Requirements

List of software, libraries, and tools needed to run the project:
- python >= 3.8
- sqlalchemy >= 2.0
- mysql-connector-python >= 9.3.0
- psycopg2 >= 2.9.0
- pandas >= 2.2.0


## Getting started

Follow the instructions below to set up the project on a local machine.


### Installation

1. Install directly from GitHub using pip:   
```bash
pip install git+https://github.com/pymetheus/sqlalchemy-dbtoolkit.git
```
2. Install dependencies:

```bash
pip install -r dep/requirements.txt
```


### Configuration

The toolkit loads database credentials and paths from the **config.ini** file:  
Populate and rename **your_config.ini** in **.config/**

```ini
[mysql]  
user = root  
password = password  
host = localhost  
port = 3306  

[postgresql]
user = postgres  
password = password  
host = localhost  
port = 5432 

[sqlite]  
sqlite_path = /path/to/sqlite/databases  
```


### Usage

Engine Factory Example:
```python
from sqlalchemy_dbtoolkit.engine.factory import AlchemyEngineFactory  

engine = AlchemyEngineFactory(dbms="mysql", db_name="analytics_db", config_path='../.config/config.ini').engine
```

ORM Table Management Example:
```python
from sqlalchemy_dbtoolkit.orm.base import ORMBaseManager
from sqlalchemy import Column, Integer, String

TableManager = ORMBaseManager(engine)
Base = TableManager.Base

class YourTable(Base):
    __tablename__ = 'your_table'
    id = Column(Integer, primary_key=True)
    column_1 = Column(String(length=255), nullable=False)
    column_2 = Column(Integer)

TableManager.create_tables()
```

ORM Session Insert Example:
```python
from sqlalchemy_dbtoolkit.query.create import InsertManager

inserter = InsertManager(engine)
inserter.add_row(YourTable, {"column_1": "value", "column_2": 42})
```

ORM Session Select Example:
```python
from sqlalchemy_dbtoolkit.query.read import SelectManager
selector = SelectManager(engine)
selection = selector.select_one_by_column(Table=YourTable, column_name="column_1", value="value")
```

Inspector Example:
```python
from sqlalchemy_dbtoolkit.core.inspector import InspectionManager
Inspector = InspectionManager(engine)
table_names = Inspector.get_table_names()
for table in table_names:
    table_columns = Inspector.get_columns(table)
```


## Roadmap

- [ ] Pandas Integration: Enable conversion between database queries and pandas DataFrames for analysis and data manipulation  
- [ ] Full CRUD Support: Expand the query layer to include read, update, and delete operations  
- [ ] SQLAlchemy Core Support: Provide additional utilities to support low-level, fine-grained database interactions  
- [ ] Integrated Logging: Add structured logging across all components to improve debugging  
- [ ] Integrate DBMSs: Include support for additional DBMS like mariadb, mssql and oracle


## Contributing

Contributions to this project are welcome! If you would like to contribute, please open an issue to discuss potential changes or submit a pull request.
For more details please visit the [contributing page](docs/CONTRIBUTING.md).


## License

This project is licensed under the [MIT License](LICENSE.md). You are free to use, modify, and distribute this code as permitted by the license.