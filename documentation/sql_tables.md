## CREATE TABLE  

```
CREATE TABLE "group" (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        PRIMARY KEY (id)
);

CREATE TABLE account (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        username VARCHAR(144) NOT NULL,
        password VARCHAR(144) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (username)
);

CREATE TABLE fish (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        species VARCHAR(144) NOT NULL,
        weight NUMERIC(4),
        image_file VARCHAR(20),
        image_blob BLOB,
        account_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(account_id) REFERENCES account (id),
        FOREIGN KEY(group_id) REFERENCES "group" (id)
);

CREATE TABLE groups (
        group_id INTEGER NOT NULL,
        account_id INTEGER NOT NULL,
        PRIMARY KEY (group_id, account_id),
        FOREIGN KEY(group_id) REFERENCES "group" (id),
        FOREIGN KEY(account_id) REFERENCES account (id)
);
```