DROP TABLE if EXISTS user;

CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL);
