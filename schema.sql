DROP TABLE if EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL UNIQUE,
    password text NOT NULL);
