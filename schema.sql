DROP TABLE if EXISTS user;

CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY,
    email text NOT NULL,
    username text NOT NULL,
    password text NOT NULL);

DROP TABLE if EXISTS songs;

CREATE TABLE songs (
    songID INTEGER NOT NULL PRIMARY KEY,
    id INTEGER NOT NULL,
    path text NOT NULL,
    title text NOT NULL,
    artist text,
    album text,
    genre text);

