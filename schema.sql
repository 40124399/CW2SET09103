DROP TABLE if EXISTS user;

CREATE TABLE user (
    id INTEGER NOT NULL AUTOINCREMENT,
    username text NOT NULL UNIQUE IGNORE,
    password text NOT NULL);
