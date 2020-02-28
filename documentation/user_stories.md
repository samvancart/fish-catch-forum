# User Stories and queries

### Completed user stories

+ User can sign up
+ User can log in
+ User can create a group
+ User can join a group
+ User can leave a group
+ User can list all groups
+ User can add posts to a specific group
+ User can list posts in specific group
+ User can view a specific post
+ User can update post
+ User can delete post
+ User can update their password
+ User can delete their profile

### User stories for future development

+ User can comment on posts

## Sql queries

+ Sign up

```
INSERT INTO account (date_created, date_modified, username, password) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)
```
+ Log in

```
SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.username AS account_username, account.password AS account_password
FROM account
WHERE account.username = ? AND account.password = ?
```
+ Create a group

```
INSERT INTO "group" (date_created, date_modified, name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)
```

+ Join group

```
INSERT INTO groups (group_id, account_id) VALUES (?, ?)
```

+ Leave group

```
DELETE FROM groups WHERE groups.group_id = ? AND groups.account_id = ?
```

+ List groups

```
SELECT "group".id AS group_id, "group".date_created AS group_date_created, "group".date_modified AS group_date_modified, "group".name AS group_name, account_1.id AS account_1_id, account_1.date_created AS account_1_date_created, account_1.date_modified AS account_1_date_modified, account_1.username AS account_1_username, account_1.password AS account_1_password
FROM "group" LEFT OUTER JOIN (groups AS groups_1 JOIN account AS account_1 ON account_1.id = groups_1.account_id) ON "group".id = groups_1.group_id
WHERE "group".id = ?
```

+ Add/update a post to a specific group

```
INSERT INTO fish (date_created, date_modified, species, weight, image_file, image_blob, account_id, group_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)
```

+ List posts in specific group

```
SELECT fish.id AS fish_id, fish.date_created AS fish_date_created, fish.date_modified AS fish_date_modified, fish.species AS fish_species, fish.weight AS fish_weight, fish.image_file AS fish_image_file, fish.image_blob AS fish_image_blob, fish.account_id AS fish_account_id, fish.group_id AS fish_group_id
FROM fish
WHERE fish.group_id = ?
```

+ View a specific post

```
SELECT "group".id AS group_id, "group".date_created AS group_date_created, "group".date_modified AS group_date_modified, "group".name AS group_name, account_?.id AS account_?_id, account_?.date_created AS account_?_date_created, account_?.date_modified AS account_?_date_modified, account_?.username AS account_?_username, account_?.password AS account_?_password
FROM "group" LEFT OUTER JOIN (groups AS groups_? JOIN account AS account_? ON account_?.id = groups_?.account_id) ON "group".id = groups_?.group_id
WHERE "group".id = ?
```

+ Delete post

```
DELETE FROM fish WHERE fish.id = ?
```


+ Update password

```
UPDATE account SET date_modified=CURRENT_TIMESTAMP, password=? WHERE account.id = ?
```

+ Delete user profile

```
DELETE FROM groups WHERE groups.group_id = ? AND groups.account_id = ?
```

```
DELETE FROM account WHERE account.id = ?
```
