DROP TABLE if EXISTS user;

CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY,
    email text NOT NULL,
    username text NOT NULL,
    password text NOT NULL);

DROP TABLE if EXISTS songs;

CREATE TABLE songs (
    id INTEGER NOT NULL PRIMARY KEY,
    userID INTEGER NOT NULL,
    path text NOT NULL,
    title text NOT NULL,
    artist text,
    album text,
    genre text);

DROP TABLE if EXISTS posts;

CREATE TABLE posts (
    id INTEGER NOT NULL PRIMARY KEY,
    userID INTEGER NOT NULL,
    title text NOT NULL,
    content text NOT NULL);
