
- Setting up user for database
```sql
CREATE DATABASE ats_app;

Use ats_app;

DROP USER IF EXISTS "ats-master";

CREATE USER 'ats-master' IDENTIFIED BY 'password';

GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, REFERENCES ON ats_app.* 
      TO 'ats-master';
      
FLUSH PRIVILEGES;
```