---
title: Managing DB with source code generator
category: database
tags:
    - database
    - mako
    - sql
    - mako
mathjax: false
comments: true
layout: single
classes: wide
published: true
---

We often write redundant codes. I personally had to write a parser for different market data protocols. This is not only tedious but also error prone. One way to tackle this problem is to normalize all data into a single in-house protocol. However, if there is a new protocol that your in-house protocol does not support, then you need to redesign your protocol which could be a pain. Additionally, you need to know all the different protocols in order to implement a normalized protocol that takes all of them into account. 

Another redundant code I had to write recently was sql code to manage database systems. While most sql databases provide a gui (pgadmin, mysql workbench), some operations take a long time that you just want to run a script in the background. Some sql codes I had to write repeatedly were 
* Modifying privileges to schema and table for each user
* Modyifying columns in tables
* Copying data into table

just to name a few.

After searching the internet and reading lots of blog posts, I've finally discovered a better way to handle redundant codes - source code generator. I've personally used Jinja2 before when using python's Django. Of the generators out there, I chose to use Mako since it has a lot of features and came after Jinja2, so it must be better than Jinja2. 

## Mako
Mako is a template code generator that takes a yaml file and a template file to generate a source code in a language of your choosing. You can find more [here][1].


## YAML file
In your yaml file, you define your parameters or the specification of your database tables. Here I have two parameters - `CREATETABLE_LST` and `GRANT_REVOKE_PRIVILEGES_TABLES_LST`. Later we will see that the generator will read the names in the list and only modify them. The database table specification is listed under `TABLES`. Depending on which database you use, you may want to change the name of the datatype and the primary key. In our example, we are using **Snowflake** database, so all the datatypes will be using the Snowflake datatypes. 

Here is an example yaml file:
```yaml
# example.yaml
CREATETABLE_LST: [
    TABLE2
]

GRANT_REVOKE_PRIVILEGES_TABLES_LST: [
    TABLE1
]

TABLES:
    TABLE1:
        SCHEMA: PUBLIC
        ROLEGRANTS:
            USER1:
                - "SELECT"
                - "INSERT"
            USER2:
                - "SELECT"
        COLUMNS:
            DATETIME:
                NULLABLE: false
                DTYPE: TIMESTAMP
                PRIMARY: true
            PID:
                NULLABLE: false
                DTYPE: BIGINT
                PRIMARY: false


    TABLE2:
        SCHEMA: PUBLIC
        ROLEGRANTS:
            USER1:
                - "SELECT"
                - "INSERT"
            USER2:
                - "SELECT"
        COLUMNS:
            DATETIME:
                NULLABLE: false
                DTYPE: TIMESTAMP
                PRIMARY: true
            VALUE:
                NULLABLE: false
                DTYPE: FLOAT
                PRIMARY: false

```

## Template SQL
Given the database specification and parameters above, we need to provide a template. Since what we want to do is create a table and modify privileges, we need the sql commands such as `CREATE TABLE` and `GRANT <privilege> ON TABLE`. As you can see below, we have those two commands wrapped around lines of code with percent signs(%) in the beginning of each line: 
```sql
-- example.sql
-- create tables
% for tablename, tabledata in TABLES.items():
    % if tablename in CREATETABLE_LST:
CREATE TABLE IF NOT EXISTS ${tabledata["SCHEMA"]}.${tablename} (
        % for i, (columnname, column) in enumerate(tabledata["COLUMNS"].items()):
            % if i == 0:
    ${columnname} ${column["DTYPE"]}
            % else:
    ,${columnname} ${column["DTYPE"]}
            % endif
        % endfor
);
    % endif
% endfor

-- grant revoke privileges to schemas
% for tablename, tabledata in TABLES.items():
    % if tablename in GRANT_REVOKE_PRIVILEGES_TABLES_LST:
        % for rolename, privileges in tabledata["ROLEGRANTS"].items():
REVOKE ALL PRIVILEGES ON TABLE ${tabledata["SCHEMA"]}.${tablename} FROM ROLE "${rolename}";
            % for privilege in privileges:
GRANT ${privilege} ON TABLE ${tabledata["SCHEMA"]}.${tablename} TO ROLE "${rolename}";
            % endfor
        % endfor
    % endif
% endfor
```
Notice that our template file contains both python and sql codes. Lines that start with a percent sign(%) are parsed by the Mako generator. The lines that do not contain the percent sign are the actual sql code that will be outputted to our resulting sql source code. 

## Generator
Generator is the tool that reads the yaml file, parses the template file and generates the sql source code. As daunting as that may sound, it only takes a few lines of python to get it done:

```python
from mako.template import Template
import sys
import yaml

templatefile = "example.sql"
datafile = "example.yaml"
template = open(templatefile, 'r').read()
config = yaml.safe_load(open(datafile, 'r'))
print(Template(template).render(**config))
```

## Generated SQL 
And we get our source code like this:
```sql
CREATE TABLE IF NOT EXISTS PUBLIC.TABLE2 (
    DATETIME TIMESTAMP
    ,VALUE FLOAT
);

-- grant revoke privileges to schemas
REVOKE ALL PRIVILEGES ON TABLE PUBLIC.TABLE1 FROM ROLE "USER1";
GRANT SELECT ON TABLE PUBLIC.TABLE1 TO ROLE "USER1";
GRANT INSERT ON TABLE PUBLIC.TABLE1 TO ROLE "USER1";
REVOKE ALL PRIVILEGES ON TABLE PUBLIC.TABLE1 FROM ROLE "USER2";
GRANT SELECT ON TABLE PUBLIC.TABLE1 TO ROLE "USER2";
```
You can try running the code locally by downloading the files at `_python/generator` in my repository.

While the above sql code is very useful when modifying privileges for different roles, when we want to upload a file or copy data into tables, it will be slow since it will run each line sequentially. 

There are way to make this faster by parallelizing it which I will discuss in the future!

[1]: https://www.makotemplates.org/
