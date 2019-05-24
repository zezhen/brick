# Budget Dashboard
Budget Dashboard for monitor and analysis

##Dashboard CI

| Build | Status |
|-------|--------|
| Component | [![Build Status](https://api.screwdriver.corp.yahoo.com:4443/badge/241939/component/icon)](https://api.screwdriver.corp.yahoo.com:4443/badge/241939/component/target) |


##Developer Guide

1. cd lib directory and run command below to install cherry-py: 
	```python ez_setup.py CherryPy-3.2.0-py2.6.egg```
2. install python dependent package
	```easy_install cherrypy pytz importlib mysql-connector```
3. install mysql server
	```yinst i mysql_server```
4. create mysql database as you want, create a table named '5m_summary' with below schema
5. copy `conf/app.cnf` to root directory then change $(db_host) $(db_user) and $(db_schema) to customed value.
6. run start.sh in shell
7. login http://hostname:4080 in browser

```sql
schema of table 5m_summary
+-----------------+----------+------+-----+---------+-------+
| Field           | Type     | Null | Key | Default | Extra |
+-----------------+----------+------+-----+---------+-------+
| time            | datetime | NO   | PRI | NULL    |       |
| mb_spend        | double   | YES  |     | NULL    |       |
| ss_spend        | double   | YES  |     | NULL    |       |
| bing_spend      | double   | YES  |     | 0       |       |
| mb_spend_usd    | double   | YES  |     | NULL    |       |
| ss_spend_usd    | double   | YES  |     | NULL    |       |
| bing_spend_usd  | double   | YES  |     | 0       |       |
| mb_budget       | double   | YES  |     | 0       |       |
| ss_budget       | double   | YES  |     | 0       |       |
| bing_only_spend | double   | YES  |     | 0       |       |
+-----------------+----------+------+-----+---------+-------+
```

**Prepare test data for your own dev box** <br/>
We have 3-day sample data (2017-03-27, 2017-04-02, 2017-04-03) for the major pmdb tables: 5m_summary, 5m_section,
revenue_triage, 5m_cmp_spend, 5m_cmp_spend_cumulative. To load them into your dev box pmdb, you need to: <br/>
1. download sample data from PhazonBlue HDFS: /projects/cb_budget/yobudget/db/sample_data.zip <br/>
2. unzip sample_data.zip on your pmdb host <br/>
3. create test tables <br/>
    ```
    mysql -u<db_user> -h<db_host> pmdb < create_tables.sql 
    ``` 
    <br/>
4. load sample data into tables <br/>
    ```
    mysql -u<db_user> -h<db_host> -e "load data local infile '`pwd`/5m_summary' replace into table 5m_summary" pmdb
    ```
    <br/>
    ```
    mysql -u<db_user> -h<db_host> -e "load data local infile '`pwd`/5m_section' replace into table 5m_section" pmdb
    ```
    <br/>
    ```
    mysql -u<db_user> -h<db_host> -e "load data local infile '`pwd`/revenue_triage' replace into table revenue_triage" pmdb
    ```
    <br/>
    ```
    mysql -u<db_user> -h<db_host> -e "load data local infile '`pwd`/5m_cmp_spend' replace into table 5m_cmp_spend" pmdb
    ```
    <br/>
    ```
    mysql -u<db_user> -h<db_host> -e "load data local infile '`pwd`/5m_cmp_spend_cumulative' replace into table 5m_cmp_spend_cumulative" pmdb
    ``` 
    <br/>

