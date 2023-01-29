---
title: Snowflake and UDFTs
category: database
tags:
    - database
    - snowflake
    - python
    - javascript
mathjax: false
comments: true
layout: single
classes: wide
published: true
---

Recently I had to do some analysis on a large dataset and sql couldn't cut it. So I had to resort using user defined function. Snowflake provides user-defined table functions(UDFTs) in four different languages, of which python seemed the easiest to me. However, it turns out python UDFTs can be either stateless or stateful. This was different from the javascript UDFTs which seem to be stateful by default. So after spending hours on stackoverflow and documentation page, I found out that to enable stateful processing in python UDFTs, I need to specify the partition. 

Here's an example of a javascript UFDT which is stateful by default:
```sql
CREATE OR REPLACE FUNCTION LAG_BY_TIME_JS(
    ROW_TIME_1 TIMESTAMP,
    CURRENT_VALUE_1 float,
)
RETURNS TABLE(
    _ROW_TIME_1 TIMESTAMP,
    _LAGGED_VALUE_1 float,
    _LAGTIMES ARRAY
)
LANGUAGE javascript
AS
$$
{
    initialize: function(argumentInfo, context) {
        this.buffer =[];
    },
    processRow: function(row, rowWriter, context) {
        this.buffer.push(
            {
                rowtime_1: row.ROW_TIME_1, 
                value_1: row.CURRENT_VALUE_1
            }
        );
        rowWriter.writeRow(
            {
                _ROW_TIME_1: row.ROW_TIME_1,
                _LAGGED_VALUE_1: row.CURRENT_VALUE_1,
                _LAGTIMES: [this.buffer.length]
            }
        )
    }
}
$$;
```
Here is a python UFDT:

```sql
CREATE OR REPLACE FUNCTION LAG_BY_TIME_PY(
    ROW_TIME TIMESTAMP,
    CURRENT_VALUE float
)
RETURNS TABLE(
    _ROW_TIME TIMESTAMP,
    _LAGGED_VALUE float,
    _LAGTIMES ARRAY
)
LANGUAGE python
RUNTIME_VERSION=3.8
PACKAGES=('numpy', 'pandas')
HANDLER='LagByTime'
AS
$$
class LagByTime:
    def __init__(self):
        self.buffer = []
    
    def process(self, rowtime, current_value, lagtimes):
        self.buffer.append((rowtime, current_value,))
        
        yield (
            self.buffer[0][0],
            self.buffer[0][1],
            [len(self.buffer)]
        )
        
    def end_partition(self):
        self.buffer = []
$$;
```
While both UFDTs may look similar, they are different in that python UFDT can be either stateful or stateless. In our case, we wish to use stateful python UDFT. In order to do that, when using our function in snowflake sql, **we need to specify the partition column**:

```sql
SELECT
     STOCK
    ,DATETIME
    ,PRICE
FROM 
    MYTABLE, 
    TABLE(
        LAG_BY_TIME_PY(
            to_epoch(DATETIME), 
            PRICE::float
        ) OVER (PARTITION BY STOCK ORDER BY DATETIME DESC)
    )
ORDER BY STOCK, DATETIME
;
```



# Other Remarks

We've recently started using snowflake to analyze our timeseries data. Having only used postgresql and mysql, it took some time for me to learn snowsql and the snowflake database. Here are some pros and cons:

## :+1: snowflake supports nanosecond precision 
Unlike postgresql or mysql that only support microsecond precision, snowflake provides nanosecond precision for their `TIMESTAMP` datatypes. This is a major plus for us since most of our analysis work requires nanosecond precision.

## :+1: snowflake does NOT enforce primary key constraint
This at first sounded like a bad idea until we realized that our data contained duplicate primary keys (we used timestamp as our primary key, even though we use nanosecond precision, there are instances where two events can occur at exactly the same time). 

## :-1: Snowflake python connector is slow
Snowflake provides a connector for python so that you can use your favorite python orms (e.g. sqlalchemy). However, my experience so far has not been great. Using snowflake connector made things at least 50% slower. It could be that converting the result to pandas dataframe takes time but for now, I'm sticking with sql on snowsql instead of python connectors. 

## :-1: Snowflake's staging and copying is very slow (with python connector)
When dealing with terabytes of data, we need fast upload and copy speed. This could be partly due to our physical distance to the datacenter (our datacenter is on the other side of the planet). However, compared to **AWS**, snowflake's uploading speed is abysmal. Additionally, once I uploaded a file to the stage, copying into the table has also been very slow. Both staging and copying were done via python connector so I may try it again with snowsql to see if it speed things up.
